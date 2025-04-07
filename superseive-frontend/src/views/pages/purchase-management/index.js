import React, { useEffect, useState } from "react";
import DataTable from "react-data-table-component";
import { Button, Card, CardBody, CardText } from "reactstrap";

//** Table Css */
import "@styles/react/libs/tables/react-dataTable-component.scss";

import useJwt from "@src/auth/jwt/useJwt";

// ** Utils

import { Edit, Plus, Trash } from "react-feather";
import { Navigate, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
const MySwal = withReactContent(Swal);
const index = () => {
  //** State */
  const [tableData, setTableData] = useState([]);

  const navigate = useNavigate();

  const handleNavigate = (uid = "") => {
    navigate("/purchase/add", { state: { clientId: uid } });
  };

  const multiLingColumns = [
    {
      name: "Company Name",
      col: "cn",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => "",
      cell: (row) => "",
    },
    {
      name: "Contact Person Name",
      col: "first_name",
      sortable: true,
      maxWidth: "350px",
      selector: (row) => "",
      cell: (row) => "",
    },
    {
      name: "Email",
      col: "email",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => "",
      cell: (row) => "",
    },
    {
      name: "Phone Number",
      col: "mobile",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => "",
      cell: (row) => "",
    },
    {
      sortable: true,
      name: "Action",
      minWidth: "90px",
      selector: (row) => "",
    },
  ];

  /* useEffect(() => {
    (async () => {
      try {
        const { data } = await useJwt.getClient();
        setTableData([...data]);
      } catch (e) {
        console.log(e);
      }
    })();
  }, []); */

  return (
    <div>
      <Card>
        <CardBody
          className={"d-flex justify-content-between align-items-center"}
        >
          <div>
            <CardText tag={"h3"}>Purchase List</CardText>
          </div>
          <Button.Ripple
            outline
            color="primary"
            onClick={() => handleNavigate()}
          >
            <Plus size={14} />
            <span className="align-middle ms-25">Purchase</span>
          </Button.Ripple>
        </CardBody>
      </Card>
      <Card>
        <DataTable
          noHeader
          subHeader
          // pagination
          responsive
          striped
          paginationPerPage={100}
          columns={multiLingColumns}
          // paginationComponent={CustomPagination}
          className="react-dataTable"
          data={tableData}
        />
      </Card>
    </div>
  );
};

export default index;
