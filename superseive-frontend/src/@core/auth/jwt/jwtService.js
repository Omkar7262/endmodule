import axios from "axios";
import jwtDefaultConfig from "./jwtDefaultConfig";
axios.defaults.baseURL = import.meta.env.VITE_REACT_APP_BASEURL;
export default class JwtService {
  // ** jwtConfig <= Will be used by this service
  jwtConfig = { ...jwtDefaultConfig };

  // ** For Refreshing Token
  isAlreadyFetchingAccessToken = false;

  // ** For Refreshing Token
  subscribers = [];

  constructor(jwtOverrideConfig) {
    this.jwtConfig = { ...this.jwtConfig, ...jwtOverrideConfig };

    // ** Request Interceptor
    axios.interceptors.request.use(
      (config) => {
        // ** Get token from localStorage
        const accessToken = this.getToken();

        // ** If token is present add it to request's Authorization Header
        if (accessToken) {
          // ** eslint-disable-next-line no-param-reassign
          config.headers.Authorization = `${
            this.jwtConfig.tokenType
          } ${accessToken.slice(1, -1)}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // ** Add request/response interceptor
    axios.interceptors.response.use(
      (response) => response,
      (error) => {
        // ** const { config, response: { status } } = error
        const { config, response } = error;
        const originalRequest = config;

        // ** if (status === 401) {
        if (response && response.status === 401) {
          if (!this.isAlreadyFetchingAccessToken) {
            this.isAlreadyFetchingAccessToken = true;
            this.refreshToken().then((r) => {
              this.isAlreadyFetchingAccessToken = false;

              // ** Update accessToken in localStorage
              this.setToken(r.data.accessToken);
              this.setRefreshToken(r.data.refreshToken);

              this.onAccessTokenFetched(r.data.accessToken);
            });
          }
          const retryOriginalRequest = new Promise((resolve) => {
            this.addSubscriber((accessToken) => {
              // ** Make sure to assign accessToken according to your response.
              // ** Check: https://pixinvent.ticksy.com/ticket/2413870
              // ** Change Authorization header
              originalRequest.headers.Authorization = `${this.jwtConfig.tokenType} ${accessToken}`;
              resolve(this.axios(originalRequest));
            });
          });
          return retryOriginalRequest;
        }
        return Promise.reject(error);
      }
    );
  }

  onAccessTokenFetched(accessToken) {
    this.subscribers = this.subscribers.filter((callback) =>
      callback(accessToken)
    );
  }

  addSubscriber(callback) {
    this.subscribers.push(callback);
  }

  getToken() {
    return localStorage.getItem(this.jwtConfig.storageTokenKeyName);
  }

  getRefreshToken() {
    return localStorage.getItem(this.jwtConfig.storageRefreshTokenKeyName);
  }

  setToken(value) {
    localStorage.setItem(this.jwtConfig.storageTokenKeyName, value);
  }

  setRefreshToken(value) {
    localStorage.setItem(this.jwtConfig.storageRefreshTokenKeyName, value);
  }

  login(...args) {
    console.log(args);
    return axios.post(this.jwtConfig.loginEndpoint, ...args);
  }

  register(...args) {
    return axios.post(this.jwtConfig.registerEndpoint, ...args);
  }

  refreshToken() {
    return axios.post(this.jwtConfig.refreshEndpoint, {
      refreshToken: this.getRefreshToken(),
    });
  }

  addVendor(...args) {
    return axios.post(this.jwtConfig.Vendor, ...args);
  }
  updateVendor(uid, ...args) {
    return axios.put(`${this.jwtConfig.Vendor}${uid}/`, ...args);
  }
  getVendor() {
    return axios.get(this.jwtConfig.Vendor);
  }
  deleteVendor(uid = "") {
    return axios.delete(`${this.jwtConfig.Vendor}${uid}/`);
  }

  addClient(...args) {
    return axios.post(this.jwtConfig.Client, ...args);
  }
  updateClient(uid, ...args) {
    return axios.put(`${this.jwtConfig.Client}${uid}/`, ...args);
  }
  getClient() {
    return axios.get(this.jwtConfig.Client);
  }
  deleteClient(uid = "") {
    return axios.delete(`${this.jwtConfig.Client}${uid}/`);
  }
  addMaster(...args) {
    return axios.post(this.jwtConfig.Master, ...args);
  }
  updateMaster(uid, ...args) {
    return axios.put(`${this.jwtConfig.Master}${uid}/`, ...args);
  }
  getMaster() {
    return axios.get(this.jwtConfig.Master);
  }
  deleteMaster(uid = "") {
    return axios.delete(`${this.jwtConfig.Master}${uid}/`);
  }
  addProductType(...args) {
    return axios.post(this.jwtConfig.ProductType, ...args);
  }
  updateProductType(uid, ...args) {
    return axios.put(`${this.jwtConfig.ProductType}${uid}/`, ...args);
  }
  getProductType() {
    return axios.get(this.jwtConfig.ProductType);
  }
  deleteProductType(uid = "") {
    return axios.delete(`${this.jwtConfig.ProductType}${uid}/`);
  }
  getVendorCategory() {
    return axios.get(this.jwtConfig.VendorCatgory);
  }

  addPackage(...args) {
    return axios.post(this.jwtConfig.Package, ...args);
  }
  updatePackage(uid, ...args) {
    return axios.put(`${this.jwtConfig.Package}${uid}/`, ...args);
  }
  getPackage() {
    return axios.get(this.jwtConfig.Package);
  }
  deletePackage(uid = "") {
    return axios.delete(`${this.jwtConfig.Package}${uid}/`);
  }

  addProduct(...args) {
    return axios.post(this.jwtConfig.Product, ...args);
  }
  updateProduct(uid, ...args) {
    return axios.put(`${this.jwtConfig.Product}${uid}/`, ...args);
  }
  getProduct() {
    return axios.get(this.jwtConfig.Product);
  }
  deleteProduct(uid = "") {
    return axios.delete(`${this.jwtConfig.Product}${uid}/`);
  }
  addInvoiceSettings(...args) {
    return axios.post(this.jwtConfig.InvoiceSettings, ...args);
  }
  updateInvoiceSettings(uid, ...args) {
    return axios.put(`${this.jwtConfig.InvoiceSettings}${uid}/`, ...args);
  }
  getInvoiceSettings() {
    return axios.get(this.jwtConfig.InvoiceSettings);
  }

  getProductListByCategoryID(id) {
    return axios.get(`${this.jwtConfig.Product}?vendor_category_id=${id}`);
  }
}
