import React, { Fragment, useEffect, useState } from "react";
import Select, { components } from "react-select";
import { useForm, Controller, useFieldArray } from "react-hook-form";
import useJwt from "@src/auth/jwt/useJwt";
import { useLocation, useNavigate } from "react-router-dom";
import { selectThemeColors } from "@utils";
import {
  Card,
  CardBody,
  Row,
  Col,
  Button,
  Form,
  Label,
  Input,
} from "reactstrap";

const accountTypeList = [
  {
    name: "Saving Account",
    id: 1,
  },
  {
    name: "Current Account",
    id: 2,
  },
];

function AddVendors(props) {
  const renderAccountType = accountTypeList.map((el) => (
    <option key={el.id} value={el.id}>
      {el.name}
    </option>
  ));
  const [vendorcategory, setVendorCategory] = useState([]);
  const [productList, setProductList] = useState([]);
  const [showProduct, setShowProduct] = useState(false);
  const [isLocalGST, setIsLocalGST] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const vendorData = location?.state?.string || {};

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      first_name: vendorData?.first_name || "",
      last_name: vendorData?.last_name || "",
      email: vendorData?.email || "",
      mobile: vendorData?.mobile || "",
      address: vendorData?.address || "",
      cn: vendorData?.cn || "",
      gst: vendorData?.gst || "",
      bn: vendorData?.bn || "",
      ac_no: vendorData?.ac_no || "",
      ac_type: vendorData?.ac_type || "",
      ifsc: vendorData?.ifsc || "",
      ahn: vendorData?.ahn || "",
      upi: vendorData?.upi || "",
      uid: vendorData?.uid || "",
      category: vendorData?.category || "",
    },
  });

  const vendorCategory = vendorcategory.map((el) => (
    <option key={el.id} value={el.id}>
      {el.name}
    </option>
  ));

  const productCategory = productList.map((el) => ({
    value: el.id,
    label: el.name,
  }));

  const {
    fields: vendorInfoList,
    append,
    remove,
  } = useFieldArray({
    name: "contactInfo",
    control,
  });

  const onSubmit = (data = {}) => {
    if (data.uid) {
      useJwt
        .updateVendor(data.uid, data)
        .then((res) => {
          if (res.status === 200) {
            navigate("/vendor/list");
          }
        })
        .catch((err) => {});
    } else {
      useJwt
        .addVendor(data)
        .then((res) => {
          if (res.status === 201) {
            navigate("/vendor/list");
          }
        })
        .catch((err) => {});
    }
  };

  function setProduct(value) {
    useJwt.getProductListByCategoryID(value).then((res) => {
      if (res?.data && res?.data.length > 0) {
        setProductList(res?.data);
        setShowProduct(true);
      } else {
        setProductList([]);
        setShowProduct(false);
      }
    });
  }

  useEffect(() => {
    (async () => {
      try {
        const { data } = await useJwt.getVendorCategory();
        setVendorCategory([...data]);
      } catch (e) {
        console.log(e);
      }
    })();
  }, []);

  return (
    <Card>
      <CardBody>
        <Form onSubmit={handleSubmit(onSubmit)}>
          {/* <Button color="primary" onClick={() => append({ firstName: '', lastName: '', email: '', phone: ''})}>
                        + Add
                    </Button> */}
          {/* {vendorInfoList.map((field, index) => ( */}

          <Row>
            <Col md="3" sm="12" className="mb-1">
              <Label className="form-label" for="first_name">
                First Name
              </Label>
              <Controller
                control={control}
                name="first_name"
                rules={{ required: "First name is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="first_name"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="3" sm="12" className="mb-1">
              <Label className="form-label" for="last_name">
                Last Name
              </Label>
              <Controller
                control={control}
                name="last_name"
                rules={{ required: "Last name is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="last_name"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="3" sm="12" className="mb-1">
              <Label className="form-label" for="email">
                Email
              </Label>
              <Controller
                control={control}
                name="email"
                rules={{ required: "Email is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="email"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="3" sm="12" className="mb-1">
              <Label className="form-label" for="mobile">
                Phone
              </Label>
              <Controller
                control={control}
                name="mobile"
                rules={{ required: "Phone is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="mobile"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>

            {/* {index != 0 ? (
              <Col sm="2" className="mb-1">
                <X onClick={() => remove(index)} />
              </Col>
            ) : (
              ""
            )} */}
          </Row>
          {/* ))} */}
          <Row>
            <Col md="12" sm="12" className="mb-1">
              <Label className="form-label" for="address">
                Address
              </Label>
              <Controller
                control={control}
                name="address"
                rules={{ required: "Address is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="textarea"
                      invalid={!!fieldState.error}
                      id="address"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="cn">
                Company Name
              </Label>
              <Controller
                control={control}
                name="cn"
                rules={{ required: "companyName is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="cn"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="gst">
                GST No
              </Label>
              <Controller
                control={control}
                name="gst"
                rules={{
                  required: "GST is required",
                  validate: (value) => {
                    if (!value.startsWith("27") && value.length > 0) {
                      setIsLocalGST(false);
                    } else if (value.startsWith("27")) {
                      setIsLocalGST(true);
                    }
                    return true; // Always returns true to avoid field error on validation
                  },
                }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="gst"
                      onChange={(e) => {
                        const value = e.target.value;

                        field.onChange(value);
                        setIsLocalGST(value.startsWith("27"));
                      }}
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="gst_value">
                {isLocalGST ? "CGST/SGST" : "IGST"}
              </Label>
              <Controller
                control={control}
                name="gst_value"
                rules={{ required: "GST Value is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      id="gst_value"
                      invalid={!!fieldState?.error}
                    ></Input>
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="category">
                Vendor Category
              </Label>
              <Controller
                control={control}
                name="category"
                rules={{ required: "Vendor Category is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="select"
                      id="category"
                      invalid={!!fieldState?.error}
                      onChange={(e) => {
                        setProduct(e.target.value, "");
                        field.onChange(e.target.value);
                      }}
                    >
                      <option value=""> Select</option>
                      {vendorCategory}
                    </Input>
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>

            {showProduct ? (
              <Col className="mb-1" md="6" sm="12">
                <Label className="form-label">Product</Label>
                <Controller
                  name="product"
                  control={control}
                  render={({ field }) => {
                    return (
                      <Select
                        options={productCategory}
                        isMulti
                        isClearable={false}
                        theme={selectThemeColors}
                        id="product"
                        style={{ border: "1px solid red !impotant" }}
                        {...field}
                        invalid={errors.payment_services && true}
                        name="colors"
                        value={productCategory.filter((option) =>
                          field.value?.some((val) => val.value === option.value)
                        )} // Match selected value(s)
                        classNamePrefix="select"
                      />
                    );
                  }}
                />
              </Col>
            ) : null}
            <Col sm="12" className="my-1">
              <h6>Bank Details</h6>
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="bn">
                Bank Name
              </Label>
              <Controller
                control={control}
                name="bn"
                rules={{ required: "Bank Name is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      id="bn"
                      invalid={!!fieldState?.error}
                    />
                    {fieldState?.error && (
                      <small className="text-danger">
                        {fieldState?.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="ac_no">
                Account No
              </Label>
              <Controller
                control={control}
                name="ac_no"
                rules={{ required: "Account No is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      id="ac_no"
                      invalid={!!fieldState?.error}
                    />
                    {fieldState?.error && (
                      <small className="text-danger">
                        {fieldState?.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="ac_type">
                Type of Account
              </Label>
              <Controller
                control={control}
                name="ac_type"
                rules={{ required: "Type Of Account is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="select"
                      id="ac_type"
                      invalid={!!fieldState?.error}
                    >
                      <option value=""> Select</option>
                      {renderAccountType}
                    </Input>
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="ifsc">
                IFSC Code
              </Label>
              <Controller
                control={control}
                name="ifsc"
                rules={{ required: "IFSC Code is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      id="ifsc"
                      invalid={!!fieldState?.error}
                    />
                    {fieldState?.error && (
                      <small className="text-danger">
                        {fieldState?.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="ahn">
                Account Holder Name
              </Label>
              <Controller
                control={control}
                name="ahn"
                rules={{ required: "Account Holder Name is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      id="ahn"
                      invalid={!!fieldState?.error}
                    />
                    {fieldState?.error && (
                      <small className="text-danger">
                        {fieldState?.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="upi">
                UPI ID
              </Label>
              <Controller
                control={control}
                name="upi"
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      id="upi"
                      invalid={!!fieldState?.error}
                    />
                    {fieldState?.error && (
                      <small className="text-danger">
                        {fieldState?.error.message}
                      </small>
                    )}
                  </Fragment>
                )}
              />
            </Col>
          </Row>
          <div className="d-flex mt-2">
            <Button className="me-1" color="primary" type="submit">
              Submit
            </Button>
            <Button
              outline
              color="secondary"
              type="reset"
              onClick={() => reset()}
            >
              Reset
            </Button>
          </div>
        </Form>
      </CardBody>
    </Card>
  );
}

export default AddVendors;
