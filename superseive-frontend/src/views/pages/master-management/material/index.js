import React, { useEffect, useState, Fragment } from "react";
import ReactPaginate from "react-paginate";
import DataTable from "react-data-table-component";
import useJwt from "@src/auth/jwt/useJwt";
import { ChevronDown, Trash, Edit } from "react-feather";
import AddEditMaster from "./addEditMaster";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";
const MySwal = withReactContent(Swal);
import {
  Card,
  CardHeader,
  CardTitle,
  Input,
  Label,
  Row,
  Col,
  Button,
  Spinner,
} from "reactstrap";
const taxTypeMapping = {
  1: "Percentage Tax",
  2: "Flat Tax",
};
function index() {
  const [openEditModel, setopenEditModel] = useState({
    isOPen: false,
    data: {},
  });
  const [currentPage, setCurrentPage] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState([]);
  const [Category, setCategory] = useState([]);
  const [Package, setPackage] = useState([]);
  function handleClick(data) {
    setopenEditModel({ isOPen: true, data: data });
  }
  const toggleModal = () =>
    setopenEditModel((previouse) => ({
      ...previouse,
      isOPen: !previouse.isOPen,
    }));
  const serverSideColumns = [
    {
      sortable: true,
      name: "Master Name",
      minWidth: "225px",
      selector: (row) => row.mn,
    },
    {
      sortable: true,
      name: "Category Name",
      minWidth: "225px",
      selector: (row) => Category.find((pkg) => pkg.id === row.category)?.name,
    },
    {
      sortable: true,
      name: "Package Name",
      minWidth: "225px",
      selector: (row) =>
        Package.find((pkg) => pkg.id === row.package)?.pck_name,
    },

    /* {
      sortable: true,
      name: "Outlet Percentage",
      minWidth: "225px",
      selector: (row) => row.outletPercentage,
    }, */

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
                  if (!row.uid) return;
                  useJwt
                    .deleteMaster(row.uid)
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
              console.log(row);

              setopenEditModel({
                isOPen: !openEditModel.isOPen,
                data: row,
              });
            }}
            style={{ margin: "5px" }}
          />
        </div>
      ),
    },
  ];
  const getTableData = async () => {
    let isLoad = true;
    setIsLoading(isLoad);
    await useJwt
      .getMaster()
      .then((res) => {
        isLoad = !isLoad;
        setData(res.data);
      })
      .catch((err) => {
        isLoad = !isLoad;
        console.log(err.response);
      });
    setIsLoading(isLoad);
  };
  const getCategory = async () => {
    await useJwt
      .getVendorCategory()
      .then((res) => {
        setCategory(res.data);
      })
      .catch((err) => {
        console.log(err.response);
      });
  };
  const getPackage = async () => {
    await useJwt
      .getPackage()
      .then((res) => {
        setPackage(res.data);
      })
      .catch((err) => {
        console.log(err.response);
      });
  };
  const dataToRender = () => {
    return data;
  };
  useEffect(() => {
    getTableData();
    getCategory();
    getPackage();
  }, []);
  // ** Custom Pagination
  const CustomPagination = () => (
    <ReactPaginate
      previousLabel={""}
      nextLabel={""}
      forcePage={currentPage}
      onPageChange={(page) => handlePagination(page)}
      pageCount={Math.ceil(dataToRender().length / 10) || 1}
      breakLabel={"..."}
      pageRangeDisplayed={2}
      marginPagesDisplayed={2}
      activeClassName="active"
      pageClassName="page-item"
      breakClassName="page-item"
      nextLinkClassName="page-link"
      pageLinkClassName="page-link"
      breakLinkClassName="page-link"
      previousLinkClassName="page-link"
      nextClassName="page-item next-item"
      previousClassName="page-item prev-item"
      containerClassName={
        "pagination react-paginate separated-pagination pagination-sm justify-content-end pe-1 mt-1"
      }
    />
  );
  return (
    <Fragment>
      <Card>
        <CardHeader className="border-bottom">
          <CardTitle tag="h4">Material List </CardTitle>
          <Row>
            <Col sm={12} md={6}>
              <Button color="primary" size="sm" onClick={() => handleClick({})}>
                Add Material
              </Button>
            </Col>
          </Row>
        </CardHeader>

        <div className="react-dataTable">
          <DataTable
            noHeader
            pagination
            columns={serverSideColumns}
            paginationPerPage={10}
            className="react-dataTable"
            sortIcon={<ChevronDown size={10} />}
            paginationDefaultPage={currentPage + 1}
            paginationComponent={CustomPagination}
            data={dataToRender()}
            progressPending={isLoading} // Use the isLoading state to indicate if data is loading
            progressComponent={
              <div className="py-2 d-flex align-items-center gap-2">
                <Spinner type="grow" color="dark" />
                <Spinner type="grow" color="dark" />
                <Spinner type="grow" color="dark" />
              </div>
            }
          />
        </div>
        <AddEditMaster
          isOpen={openEditModel.isOPen}
          setOpen={toggleModal}
          updateData={openEditModel.data}
          Category={Category}
          Package={Package}
        />
      </Card>
    </Fragment>
  );
}

export default index;
