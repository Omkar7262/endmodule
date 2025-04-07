// ** Auth Endpoints
export default {
  loginEndpoint: "/api/login",
  registerEndpoint: "/jwt/register",
  refreshEndpoint: "/jwt/refresh-token",
  logoutEndpoint: "/jwt/logout",
  Vendor: "/api/vn/",
  VendorCatgory: "/api/vnc/",
  Package: "/api/pck/",
  Product: "/api/pd/",
  Client: "/api/clt/",
  Master: "/api/mt/",
  ProductType: "/api/pt/",
  InvoiceSettings: "/api/ins/",
  // ** This will be prefixed in authorization header with token
  // ? e.g. Authorization: Bearer <token>
  tokenType: "Bearer",

  // ** Value of this property will be used as key to store JWT token in storage
  storageTokenKeyName: "accessToken",
  storageRefreshTokenKeyName: "refreshToken",
};
