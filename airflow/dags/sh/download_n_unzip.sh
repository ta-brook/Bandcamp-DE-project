# download data from source
SAVE_NAME=$1
AIRFLOW_HOME=$2

URL="https://www.dropbox.com/s/wd38q80el16i19q/1000000-bandcamp-sales.zip?dl=1"
SAVE_DIRECTORY="data"
ZIP='zip'
CSV='csv'

echo "making directory... ${AIRFLOW_HOME}/${SAVE_DIRECTORY}"
mkdir "${AIRFLOW_HOME}/${SAVE_DIRECTORY}"
SAVE_FULL_PATH="${AIRFLOW_HOME}/${SAVE_DIRECTORY}/${SAVE_NAME}.${ZIP}"

echo "Downloading..."
wget "${URL}" -O "${SAVE_FULL_PATH}"

echo "Unpacking data..."
cd "${AIRFLOW_HOME}/${SAVE_DIRECTORY}"
unzip -p "${SAVE_NAME}" > "${SAVE_NAME}.${CSV}"

echo "removing zip file"
rm "${SAVE_NAME}.${ZIP}" 
echo "Done"