import sys
from pyspark.sql import SparkSession
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import LogisticRegressionModel 
# --- NEW IMPORT ---
from pyspark.ml.feature import VectorAssembler 

# --- Configuration ---
MODEL_PATH = "wine_quality_model" 
LABEL_COLUMN = "quality"

def predict_and_evaluate(input_filepath):
    """
    Initializes Spark, loads the model, makes predictions on the test data, 
    and prints the F1 score.
    """
    # Create Spark Session
    spark = SparkSession.builder \
        .appName("WineQualityPrediction") \
        .getOrCreate()

    print("-" * 50)
    print(f"Loading data from: {input_filepath}")
    
    # 1. Load Test Data
    try:
        df = spark.read.csv(
            input_filepath, 
            header=True, 
            inferSchema=True, 
            sep=";", 
            quote='"'
        )
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        spark.stop()
        print(f"Check that the file path {input_filepath} is correct and accessible via the volume mount.")
        sys.exit(1)

    # --- CRITICAL FIX 1: Clean up column names by stripping extra quotes ---
    # The error message showed names like """"fixed acidity"""", so we clean them up.
    for col_name in df.columns:
        # Strip all leading/trailing double quotes
        new_col_name = col_name.strip('"')
        if col_name != new_col_name:
            df = df.withColumnRenamed(col_name, new_col_name)

    # 2. Load the trained Model
    try:
        model = LogisticRegressionModel.load(MODEL_PATH) 
        print(f"Successfully loaded model from: {MODEL_PATH}")
    except Exception as e:
        print(f"Error loading model: {e}")
        spark.stop()
        sys.exit(1)
        
    # --- CRITICAL FIX 2: Add VectorAssembler to create the 'features' column ---
    # This replaces the missing step from the original PipelineModel.
    feature_cols = [col for col in df.columns if col != LABEL_COLUMN]
    
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    
    # Transform the DataFrame to create the required 'features' vector
    df = assembler.transform(df)
    
    # 3. Make Predictions
    predictions = model.transform(df)
    
    # 4. Evaluate Model Performance (F1 Score)
    evaluator = MulticlassClassificationEvaluator(
        labelCol=LABEL_COLUMN, 
        predictionCol="prediction", 
        metricName="f1"
    )
    f1_score = evaluator.evaluate(predictions)

    # 5. Output Result
    print("-" * 50)
    print(f"✅ Prediction F1 Score on Test Data: {f1_score:.4f}")
    print("-" * 50)

    spark.stop()

if __name__ == "__main__":
    try:
        test_filepath = sys.argv[1]
    except IndexError:
        print("Error: No file path argument provided.")
        print("Usage: sudo docker run ... wine-predictor:latest /app/data/ValidationDataset.csv")
        sys.exit(1)
        
    predict_and_evaluate(test_filepath)
