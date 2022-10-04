cd src

set -e

if [ ! -f ../config/.env ]; then
  source ../config/properties.env
fi

set +e

if [ ! -d ./model ]; then
  mkdir ./model
else
  echo "File Exists!"
fi

streamlit run app.py &
uvicorn app:app --env-file="../config/properties.env" --reload
#uvicorn app:app --env-file="../config/properties.env" --host 0.0.0.0 --port 8565 --workers 1 --reload

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?