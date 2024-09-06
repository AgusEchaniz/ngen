import axios from "axios";
import apiInstance from "./api";
import { refreshToken } from "./services/auth";
import setAlert from "../utils/setAlert";
import { LOGOUT } from "../store/actions";

const setup = (store) => {
  let isRefreshing = false;
  let refreshSubscribers = [];

  const subscribeTokenRefresh = (cb) => {
    refreshSubscribers.push(cb);
  };

  const onRefreshed = (token) => {
    refreshSubscribers.map((cb) => cb(token));
  };

  apiInstance.interceptors.request.use((request) => {
    const state = store.getState();
    const token = state.account.token;

    if (request.url.includes("refresh")) {
      delete apiInstance.defaults.headers.common["Authorization"];
    } else if (token) {
      request.headers.Authorization = `Bearer ${token}`;
      apiInstance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }

    return request;
  });

  apiInstance.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      if (error.response === undefined) {
        // setAlert("Falló la conexión al servidor backend", "error", "api"); NO FUNCIONA
        console.log("Falló la conexión al servidor");
        return Promise.reject(error);
      }

      const originalRequest = error.config;

      if (
        error.response.data.code === "token_not_valid" &&
        !originalRequest._retry &&
        !JSON.stringify(originalRequest.url).includes("refresh")
      ) {
        originalRequest._retry = true;

        if (!isRefreshing) {
          isRefreshing = true;
          refreshToken()
            .then((response) => {
              let newToken = response.data.access;
              onRefreshed(newToken);
            })
            .catch(() => {
              store.dispatch({
                type: LOGOUT
              });
              setAlert("Su sesión ha expirado", "error");
            })
            .finally(() => {
              refreshSubscribers = [];
              isRefreshing = false;
            });
        }

        return new Promise((resolve) => {
          subscribeTokenRefresh((token) => {
            // replace the expired token and retry
            originalRequest.headers["Authorization"] = "Bearer " + token;
            return resolve(axios(originalRequest));
          });
        });
      } else {
        console.log("Error en el setup-interceptor");
        console.log(error);
        return Promise.reject(error);
      }
    }
  );
};

export default setup;
