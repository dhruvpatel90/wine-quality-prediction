from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Initialize Spark
spark = SparkSession.builder \
    .appName("WineQualityTraining") \
    .getOrCreate()

print("Loading training data...")
# Load training data - handle quotes properly
train_df = spark.read.csv("/home/ubuntu/TrainingDataset.csv", header=True, inferSchema=True, sep=";", quote='"')

print("Loading validation data...")
# Load validation data
val_df = spark.read.csv("/home/ubuntu/ValidationDataset.csv", header=True, inferSchema=True, sep=";", quote='"')

# Clean column names (remove quotes)
for col in train_df.columns:
    train_df = train_df.withColumnRenamed(col, col.replace('"', '').strip())
for col in val_df.columns:
    val_df = val_df.withColumnRenamed(col, col.replace('"', '').strip())

print("Columns:", train_df.columns)

# Get feature columns (all except quality)
feature_cols = [col for col in train_df.columns if col != 'quality']

# Create feature vector
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
train_data = assembler.transform(train_df).select("features", "quality")
val_data = assembler.transform(val_df).select("features", "quality")

print("Training logistic regression model...")
# Train model
lr = LogisticRegression(featuresCol="features", labelCol="quality", maxIter=100)
model = lr.fit(train_data)

print("Evaluating model on validation data...")
# Make predictions
predictions = model.transform(val_data)

# Evaluate
evaluator = MulticlassClassificationEvaluator(labelCol="quality", predictionCol="prediction", metricName="f1")
f1_score = evaluator.evaluate(predictions)

print(f"\n=== Model Performance ===")
print(f"F1 Score on Validation Data: {f1_score:.4f}")

# Save model
model_path = "wine_quality_model"
print(f"\nSaving model to {model_path}...")
model.write().overwrite().save(model_path)

print("Training completed successfully!")

spark.stop()
