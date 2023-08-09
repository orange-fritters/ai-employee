To deploy your Docker container on Google Cloud Platform (GCP) using Cloud Run, you'll follow these steps:

1. **Ensure that the `gcloud` command-line tool is set up**: Make sure you've [installed `gcloud`](https://cloud.google.com/sdk/docs/quickstarts) and authenticated it using:

   ```
   gcloud auth login
   ```

2. **Configure Docker to use `gcloud` as a credential helper**:

   ```
   gcloud auth configure-docker
   ```

3. **Tag the Docker image**:

   Before you can push the image to the Google Container Registry (GCR), you need to tag it with a specific format.

   ```
   docker tag ai-employee gcr.io/ai-employee-welfare-service/ai-employee:latest
   ```

4. **Push the Docker image to GCR**:

   This will upload your local Docker image to the Google Container Registry.

   ```
   docker push gcr.io/ai-employee-welfare-service/ai-employee:latest
   ```

5. **Deploy to Cloud Run**:

   With the image now on GCR, you can deploy it to Cloud Run.

   ```
   gcloud run deploy ai-employee-service \
   --image gcr.io/ai-employee-welfare-service/ai-employee:latest \
   --platform managed \
   --region asia-northeast3
   --set-env-vars OPENAI_API_KEY=your_openai_api_key
   ```

   - Here, `ai-employee-service` is the name of the Cloud Run service. You can change this to your desired name.
   - `--platform managed` specifies that you're using the fully managed version of Cloud Run.
   - `--region asia-northeast3` sets the deployment region. You can change this to a region closer to your primary users.

6. **Finish Deployment**:

   `gcloud` might prompt you to allow unauthenticated invocations, you can choose 'yes' or 'no' based on your preference. If you choose 'yes', anyone can access the Cloud Run service, if you choose 'no', only authenticated users can access it.

After deployment, `gcloud` will provide a URL for your live service. You can visit that URL to access your deployed application.

Remember, every time you make changes to your application and want to redeploy, you'll need to rebuild the Docker image, push it to GCR, and then deploy it to Cloud Run again.
