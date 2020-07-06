gcloud functions deploy cloud-tqdm --entry-point main --runtime python37 --source . \
       --trigger-http --allow-unauthenticated --memory 128MB --region asia-northeast1 --project cloud-tqdm
