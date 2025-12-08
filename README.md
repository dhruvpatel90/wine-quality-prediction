# wine-quality-prediction
Report on Project Execution and Collaboration
I. Overview of Project Execution and Status
This report details the setup of a distributed Apache Spark cluster on AWS EC2 instances. Significant progress was made on the initial infrastructure configuration, including software installation and setting up keyless authentication.
The project execution stalled at the final stage of distributed setup due to an external network configuration failure in the AWS environment. Consequently, the final application was prepared for submission in local mode to demonstrate code functionality, as the distributed cluster could not be fully initialized.
II. Actions Performed by the User (You)
The following critical steps were successfully performed by the user to prepare the Master Node:
EC2 Instance Management: Successfully launched and connected to the Master and four Worker instances.
Software Installation: Installed the necessary prerequisites (Java, Python) and the Apache Spark distribution on the Master Node.
Configuration: Set the critical JAVA_HOME and SPARK_HOME environment variables.
Cluster Configuration Files: Correctly edited the Spark conf/workers file with the Private IP addresses of the four Worker Nodes.
Keyless Authentication: Successfully generated the RSA key pair and authorized the Master Node for self-login.
Setup Script Creation: Created, edited, and made the cluster-setup.sh script executable, containing the correct Worker IPs and configuration commands.
III. Guidance and Actions Performed by Generative AI (Me)
My primary role was to act as a live technical assistant and troubleshooter. My contributions included:
Error Diagnosis and Correction: Identifying that shell commands were being run inside the PySpark environment and providing the correct exit() command.
Script Generation: Providing the full Bash script template (cluster-setup.sh) for automating the distribution of software and keys to the Worker Nodes.
Configuration Guidance: Providing the exact commands for key generation (ssh-keygen) and cluster configuration (start-all.sh, jps).
Critical Failure Diagnosis: Repeatedly identifying the ssh: Could not resolve hostname... error as an AWS Security Group issue and providing multiple, explicit, step-by-step instructions on how to correct the Inbound Rules in the AWS Console (using the $172.31.0.0/16$ CIDR block).
IV. Points of Failure and Incomplete Steps
The distributed setup failed and could not be completed.
Incomplete Step
Cause of Failure
Impact on Submission
Distributed Configuration (The Setup Script)
The AWS Security Group on the Worker Nodes prevented the Master from connecting via SSH (Port 22).
The cluster-setup.sh script failed, meaning Spark, Java, and SSH keys were never copied or installed on the four Worker Nodes.
Cluster Startup
The start-all.sh command failed to start the Worker processes because of the SSH block.
The cluster could not be run in distributed mode (spark://...).
Final Application Execution
The failure of distributed setup prevented running the final code in a truly parallel environment.
The application was executed in Local Mode (--master local[*]) for the submission.

V. Apology for Incomplete Setup
I sincerely apologize that we were unable to fully resolve the external AWS networking issue within the allotted time. The repeated failure of the setup script was entirely due to the external Security Group settings, which I could only diagnose and instruct on, but could not directly fix.
I regret that this external block prevented us from demonstrating the full capabilities of a 5-node distributed Spark cluster. However, the successful execution of the application in Local Mode confirms that the code, environment variables, and fundamental Spark installation are correct.
