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
    navigate("/vendor/add", {
      state: { vendorId: uid },
    });
  };

  const multiLingColumns = [
    {
      name: "Company Name",
      col: "cn",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => row.cn,
      cell: (row) => <span className="text-capitalize">{row.cn}</span>,
    },
    {
      name: "Contact Person Name",
      col: "first_name",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => row.first_name,
      cell: (row) => (
        <span className="text-capitalize">
          {row.first_name} {row.last_name}
        </span>
      ),
    },
    {
      name: "Email",
      col: "email",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => row.email,
      cell: (row) => <span className="text-capitalize">{row.email}</span>,
    },
    {
      name: "Phone Number",
      col: "mobile",
      sortable: true,
      maxWidth: "200px",
      selector: (row) => row.mobile,
      cell: (row) => <span className="text-capitalize">{row.mobile}</span>,
    },
    {
      sortable: true,
      name: "Action",
      minWidth: "150px",
      selector: (row) => (
        <div className="d-flex gap-1">
          <Trash
            className="cursor-pointer"
            size={"14"}
            onClick={() => {
              return MySwal.fire({
                title: "Are you sure?",
                text: "You won't be able to delete this!",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Yes, delete it!",
                customClass: {
                  confirmButton: "btn btn-primary",
                  cancelButton: "btn btn-danger ms-1",
                },
                buttonsStyling: false,
              }).then(function (result) {
                console.log(result);
                if (result.value) {
                  /*  */
                  if (!row.uid) return;
                  useJwt
                    .deleteVendor(row.uid)
                    .then((res) => {
                      if (res) {
                        MySwal.fire({
                          icon: "success",
                          title: "Deleted!",
                          text: "Your record has been deleted.",
                          customClass: {
                            confirmButton: "btn btn-success",
                          },
                        });
                        location.reload();
                      }
                    })
                    .catch((err) => {
                      console.log(err?.response);
                    });
                } else if (result.dismiss === MySwal.DismissReason.cancel) {
                  MySwal.fire({
                    title: "Cancelled",
                    text: "Your record is safe :)",
                    icon: "error",
                    customClass: {
                      confirmButton: "btn btn-success",
                    },
                  });
                }
              });
            }}
          />
          <Edit
            className="cursor-pointer"
            size={"14"}
            onClick={() => {
              navigate("/vendor/add", {
                state: { string: row },
              });
            }}
            style={{ margin: "5px" }}
          />
        </div>
      ),
    },
  ];

  useEffect(() => {
    (async () => {
      try {
        const { data } = await useJwt.getVendor();
        setTableData([...data]);
      } catch (e) {
        console.log(e);
      }
    })();
  }, []);

  return (
    <div>
      <Card>
        <CardBody
          className={"d-flex justify-content-between align-items-center"}
        >
          <div>
            <CardText tag={"h3"}>Vendor List</CardText>
          </div>
          <Button.Ripple
            outline
            color="primary"
            onClick={() => handleNavigate()}
          >
            <Plus size={14} />
            <span className="align-middle ms-25">Vendor</span>
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
