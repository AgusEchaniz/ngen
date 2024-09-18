import apiInstance from "../api";
import { COMPONENT_URL } from "../../config/constant";
import setAlert from "../../utils/setAlert";

const getProfile = () => {
  let messageError = `No se ha recuperado la informacion del usuario. `;
  return apiInstance
    .get(COMPONENT_URL.profile)
    .then((response) => {
      return response;
    })
    .catch((error) => {
      let statusText = error.response.statusText;
      messageError += statusText;
      setAlert(messageError, "error", "report");
      return Promise.reject(error);
    });
};

const getApiKey = (username, password) => {
  let messageError = `No se ha recuperado la api key del usuario. `;
  return apiInstance
    .post(COMPONENT_URL.apikey, {
      username: username,
      password: password,
    })
    .then((response) => {
      return response;
    })
    .catch((error) => {
      let statusText = error.response.statusText;
      messageError += statusText;
      setAlert(messageError, "error", "report");
      return Promise.reject(error);
    });
}

export { getProfile, getApiKey };
