import React, { Fragment } from "react";
import useJwt from "@src/auth/jwt/useJwt";
import { useLocation, useNavigate } from "react-router-dom";
import { useForm, Controller, useFieldArray } from "react-hook-form";
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
function AddVendors() {
  const renderAccountType = accountTypeList.map((el) => (
    <option key={el.id} value={el.id}>
      {el.name}
    </option>
  ));
  const location = useLocation();
  const navigate = useNavigate();

  const vendorData = location?.state?.string || {};
  console.log(vendorData);
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
      ac_type: vendorData?.ac_type || 0,
      ifsc: vendorData?.ifsc || "",
      ahn: vendorData?.ahn || "",
      upi: vendorData?.upi || "",
      uid: vendorData?.uid || "",
    },
  });

  const {
    fields: vendorInfoList,
    append,
    remove,
  } = useFieldArray({
    name: "contactInfo",
    control,
  });

  const onSubmit = (data = {}) => {
    console.log(data);

    if (data.uid) {
      useJwt
        .updateClient(data.uid, data)
        .then((res) => {
          if (res.status === 200) {
            navigate("/client/list");
          }
        })
        .catch((err) => {});
    } else {
      useJwt
        .addClient(data)
        .then((res) => {
          if (res.status === 201) {
            navigate("/client/list");
          }
        })
        .catch((err) => {});
    }
  };

  return (
    <Card>
      <CardBody>
        <Form onSubmit={handleSubmit(onSubmit)}>
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
          </Row>

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
                rules={{ required: "GST is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="gst"
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
              <Label className="form-label" for="aac_typet">
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
