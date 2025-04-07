import { lazy } from "react";

const VendorManagement = lazy(() =>
  import("../../views/pages/vendor-management")
);

const VendorAdd = lazy(() => import("../../views/pages/vendor-management/add"));
const ClientManagement = lazy(() =>
  import("../../views/pages/client-management")
);

const ClientAdd = lazy(() => import("../../views/pages/client-management/add"));
const Material = lazy(() =>
  import("../../views/pages/master-management/material")
);
const MasterManagement = lazy(() =>
  import("../../views/pages/master-management")
);
const ProductTypes = lazy(() =>
  import("../../views/pages/master-management/product-type")
);

const PackageTypes = lazy(() =>
  import("../../views/pages/master-management/package-type")
);

const PurchaseManagement = lazy(() =>
  import("../../views/pages/purchase-management")
);

const PurchaseAdd = lazy(() =>
  import("../../views/pages/purchase-management/add")
);

const Product = lazy(() => import("../../views/pages/product"));
const InvoiceSetting = lazy(() =>
  import("../../views/pages/settings/invoice-settings")
);

const DashboardRoutes = [
  {
    path: "/vendor/list",
    element: <VendorManagement />,
    meta: {
      action: "read",
      resource: "vendor-management",
    },
  },
  {
    path: "/vendor/add",
    element: <VendorAdd />,
    meta: {
      action: "read",
      resource: "vendor-management",
    },
  },
  {
    path: "/client/list",
    element: <ClientManagement />,
    meta: {
      action: "read",
      resource: "client-management",
    },
  },
  {
    path: "/client/add",
    element: <ClientAdd />,
    meta: {
      action: "read",
      resource: "client-management",
    },
  },
  {
    path: "/admin/master",
    element: <MasterManagement />,
    meta: {
      action: "read",
      resource: "master-management",
    },
  },
  {
    path: "master/package-type/",
    element: <PackageTypes />,
    meta: {
      action: "read",
      resource: "master",
    },
  },
  {
    path: "master/material/",
    element: <Material />,
    meta: {
      action: "read",
      resource: "master",
    },
  },
  {
    path: "master/product-type/",
    element: <ProductTypes />,
    meta: {
      action: "read",
      resource: "master",
    },
  },
  {
    path: "purchase/list/",
    element: <PurchaseManagement />,
    meta: {
      action: "read",
      resource: "purchase-management",
    },
  },
  {
    path: "/purchase/add",
    element: <PurchaseAdd />,
    meta: {
      action: "read",
      resource: "purchase-management",
    },
  },
  {
    path: "/product/list",
    element: <Product />,
    meta: {
      action: "read",
      resource: "product-management",
    },
  },
  {
    path: "settings/invoice-settings/",
    element: <InvoiceSetting />,
    meta: {
      action: "read",
      resource: "settings",
    },
  },
];
export default DashboardRoutes;
