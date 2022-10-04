set -e

if [ ! -f ./config/.env ]; then
  source ./config/properties.env
fi

set +e

if [ ! -d ./model ]; then
  mkdir .model
else
  echo "File Exists!"
fi

#streamlit run app.py --server.port=8565
uvicorn app:app --env-file=".\config\properties.env" --port=8565 --workers=1 --reload
