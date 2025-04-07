import React, { Fragment, useEffect, useState } from "react";

import { useForm, Controller } from "react-hook-form";
import useJwt from "@src/auth/jwt/useJwt";
import toast from "react-hot-toast";
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

function index() {
  const [invoiceData, setInvoiceData] = useState([]);
  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      invoiceNumType: "",
      invoicePrefix: "",
      invoiceSign: [], // Change to an empty array
      invoiceLogo: [], // Change to an empty array
      notes: "",
      terms: "",
      uid: "",
    },
  });
  const onSubmit = async (data) => {
    const formData = new FormData();
    /* Object.keys(data).map((key) => {
      if ((key == "sign" || key == "logo") && data[key]?.[0])
        formData.append(key, data[key][0]);
      else if (data[key]) formData.append(key, data[key]);
    }); */
    Object.keys(data).forEach((key) => {
      if (key === "sign" || key === "logo") {
        // Append files if selected
        if (data[key]?.[0]) {
          formData.append(key, data[key][0]);
        } else {
          console.error(`${key} is required but not provided.`);
        }
      } else {
        formData.append(key, data[key]);
      }
    });
    if (data.uid) {
      formData.append("uid", data.uid);
    }

    try {
      let responseData;
      let response;
      if (data.uid) {
        response = await useJwt.updateInvoiceSettings(data.uid, formData);
      } else {
        response = await useJwt.addInvoiceSettings(formData);
      }

      if (response.status === 200 || response.status === 201) {
        responseData = response.data;
        toast.success("Invoice Settings Created Successfully");
        location.reload();
      } else {
        toast.error("Error creating invoice settings");
        console.log(`Unexpected response status: ${response.status}`);
      }
    } catch (e) {
      console.log(e);
      toast.error("Unable to create invoice settings ");
    }
  };

  useEffect(() => {
    (async () => {
      try {
        const { data } = await useJwt.getInvoiceSettings();
        if (data.length > 0) {
          const invoiceSettings = data[0]; // Take the first record if it’s a single result

          // Set form fields with the fetched data
          reset({
            invoiceNoType: invoiceSettings.invoiceNoType.toString(), // Convert number to string for radio button
            prefix: invoiceSettings.prefix || "",
            notes: invoiceSettings.notes || "",
            terms: invoiceSettings.terms || "",
            uid: invoiceSettings.uid || "", // If you have a UID, you can use it to update the invoice settings
          });

          // Optional: Set image URLs or other data for display
          setInvoiceData({
            sign: invoiceSettings.sign,
            logo: invoiceSettings.logo,
          });
        }
      } catch (e) {
        console.log(e);
      }
    })();
  }, [reset]);

  return (
    <Card>
      <CardBody>
        <Form onSubmit={handleSubmit(onSubmit)} encType="multipart/form-data">
          <Row>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="invoiceNoType">
                Invoice Number Type
              </Label>
              <Controller
                control={control}
                name="invoiceNoType"
                rules={{ required: "Invoice number type is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <div className="form-check">
                      <Input
                        {...field}
                        type="radio"
                        id="invoiceNoType1"
                        value="1"
                        checked={field.value === "1"}
                        className="form-check-input"
                      />
                      <Label for="invoiceNoType1" className="form-check-label">
                        Sequense
                      </Label>
                    </div>
                    <div className="form-check">
                      <Input
                        {...field}
                        type="radio"
                        id="invoiceNoType2"
                        value="2"
                        checked={field.value === "2"}
                        className="form-check-input"
                      />
                      <Label for="invoiceNoType2" className="form-check-label">
                        Random
                      </Label>
                    </div>
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
              <Label className="form-label" for="prefix">
                Invoice Prefix
              </Label>
              <Controller
                control={control}
                name="prefix"
                rules={{ required: "Invoice prefix is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="text"
                      invalid={!!fieldState.error}
                      id="prefix"
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
              <Label className="form-label" for="sign">
                Invoice Signature
              </Label>
              <Controller
                control={control}
                name="sign"
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      type="file"
                      invalid={!!fieldState.error}
                      onChange={(e) => field.onChange(e.target.files)}
                      id="sign"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                    {invoiceData.sign && (
                      <img
                        src={invoiceData.sign}
                        alt="Invoice Sign"
                        style={{ maxWidth: "100px", marginTop: "10px" }}
                      />
                    )}
                  </Fragment>
                )}
              />
            </Col>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="logo">
                Invoice Logo
              </Label>
              <Controller
                control={control}
                name="logo"
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      type="file"
                      onChange={(e) => field.onChange(e.target.files)}
                      invalid={!!fieldState.error}
                      id="logo"
                    />
                    {fieldState.error && (
                      <small className="text-danger">
                        {fieldState.error.message}
                      </small>
                    )}
                    {invoiceData.logo && (
                      <img
                        src={invoiceData.logo}
                        alt="Invoice Logo"
                        style={{ maxWidth: "100px", marginTop: "10px" }}
                      />
                    )}
                  </Fragment>
                )}
              />
            </Col>
          </Row>

          <Row>
            <Col md="6" sm="12" className="mb-1">
              <Label className="form-label" for="notes">
                Invoice Notes
              </Label>
              <Controller
                control={control}
                name="notes"
                rules={{ required: "Notes is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="textarea"
                      invalid={!!fieldState.error}
                      id="notes"
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
              <Label className="form-label" for="terms">
                Invoice Terms and Conditions
              </Label>
              <Controller
                control={control}
                name="terms"
                rules={{ required: "Terms and Conditions is required" }}
                render={({ field, fieldState }) => (
                  <Fragment>
                    <Input
                      {...field}
                      type="textarea"
                      invalid={!!fieldState.error}
                      id="terms"
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

export default index;
