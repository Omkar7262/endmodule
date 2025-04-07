import { Circle, Server, ShoppingCart } from "react-feather";

export default [
  {
    id: "vendorManagement",
    title: "Vendor",
    icon: <Server size={20} />,
    navLink: "/vendor/list",
    action: "read",
    resource: "vendor-management",
  },
  {
    id: "clientManagement",
    title: "Client",
    icon: <Server size={20} />,
    navLink: "/client/list",
    action: "read",
    resource: "client-management",
  },
  {
    id: "masterManagement",
    title: "Master Data",
    icon: <Server size={20} />,
    children: [
      {
        id: "package-type",
        title: "Package Type",
        icon: <Circle size={12} />,
        navLink: "/master/package-type/",
        action: "read",
        resource: "package-type",
      },
      {
        id: "material",
        title: "Material",
        icon: <Circle size={12} />,
        navLink: "/master/material/",
        action: "read",
        resource: "material",
      },
      {
        id: "product-type",
        title: "Product Type",
        icon: <Circle size={12} />,
        navLink: "/master/product-type/",
        action: "read",
        resource: "product-type",
      },
    ],
  },
  {
    id: "productManagement",
    title: "Product",
    icon: <Server size={20} />,
    navLink: "/product/list",
    action: "read",
    resource: "product-management",
  },
  {
    id: "settings",
    title: "Settings",
    icon: <Server size={20} />,
    children: [
      {
        id: "invoice-settings",
        title: "Invoice Setting",
        icon: <Circle size={12} />,
        navLink: "/settings/invoice-settings/",
        action: "read",
        resource: "invoice-settings",
      },
    ],
  },
  {
    id: "purchaseManagement",
    title: "Purchase",
    icon: <Server size={20} />,
    navLink: "/purchase/list",
    action: "read",
    resource: "purchase-management",
  },
];
