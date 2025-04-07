import { React, Fragment, useState, useEffect } from "react";
import useJwt from "@src/auth/jwt/useJwt";
import { Controller, useForm } from "react-hook-form";
import {
  Row,
  Col,
  Modal,
  Input,
  Label,
  Button,
  ModalBody,
  ModalHeader,
  FormFeedback,
  Form,
} from "reactstrap";
import { User, Check, X } from "react-feather";
import Select from "react-select";
import { selectThemeColors } from "@utils";
const options = [
  { value: "1", label: "Percentage" },
  { value: "2", label: "Flat" },
];
const addEditMaster = (props) => {
  const { isOpen, setOpen, updateData, material, productType } = props;

  const [show, setShow] = useState(false);
  const {
    control,
    setError,
    clearErrors,
    handleSubmit,
    formState: { errors },
    getValues,
    setValue,
    watch,
    reset,
  } = useForm({});
  const CloseBtn = (
    <X className="cursor-pointer" size={15} onClick={() => setOpen(!open)} />
  );

  const materialArr = material.map((el) => (
    <option key={el.id} value={el.id}>
      {el.mn}
    </option>
  ));

  const productTypeArr = productType.map((el) => (
    <option key={el.id} value={el.id}>
      {el.pt}
    </option>
  ));

  const onSubmit = (data = {}) => {
    if (data.uid) {
      useJwt
        .updateProduct(data.uid, data)
        .then((res) => {
          if (res.status === 200) {
            location.reload();
          }
        })
        .catch((err) => {});
    } else {
      useJwt
        .addProduct(data)
        .then((res) => {
          if (res.status === 201) {
            location.reload();
          }
        })
        .catch((err) => {});
    }
  };
  const handleEditeData = async (data) => {
    try {
      return data;
    } catch (e) {
      throw e;
    }
  };

  useEffect(() => {
    if (Object.keys(updateData)?.length > 0) {
      handleEditeData(updateData)
        .then((data) => {
          reset({ ...data });
        })
        .catch((e) => {
          console.log({ e });
        });
    }
    return () => {
      reset();
    };
  }, [updateData, isOpen, reset]);

  return (
    <Fragment>
      <Modal isOpen={isOpen} className="modal-dialog-centered modal-lg">
        <ModalHeader
          className="bg-transparent"
          toggle={() => setOpen()}
        ></ModalHeader>
        <ModalBody className="px-sm-5 mx-50 pb-5">
          <div className="text-center mb-2">
            <h1 className="mb-1"> Product Info</h1>
          </div>

          <Form onSubmit={handleSubmit(onSubmit)}>
            <Row>
              <Col md="6" sm="12" className="mb-1">
                <Label className="form-label" for="name">
                  Product Name <span className="text-danger">*</span>
                </Label>
                <Controller
                  control={control}
                  name="name"
                  rules={{
                    required: "This Field is Required",
                  }}
                  render={({ field }) => {
                    return (
                      <Input
                        {...field}
                        id="name"
                        placeholder=""
                        value={field.value || ""}
                        invalid={errors.mn && true}
                      />
                    );
                  }}
                />
                {errors.mn && (
                  <FormFeedback>Please enter product name</FormFeedback>
                )}
              </Col>

              <Col md="6" sm="12" className="mb-1">
                <Label className="form-label" for="gauge">
                  Gauge<span className="text-danger">*</span>
                </Label>
                <Controller
                  control={control}
                  name="gauge"
                  render={({ field }) => {
                    return (
                      <Input
                        {...field}
                        id="gauge"
                        placeholder=""
                        value={field.value || ""}
                        invalid={errors.mn && true}
                      />
                    );
                  }}
                />
                {errors.mn && <FormFeedback>Please enter gauge</FormFeedback>}
              </Col>

              <Col md="6" sm="12" className="mb-1">
                <Label className="form-label" for="pt">
                  Product Type
                </Label>
                <Controller
                  control={control}
                  name="pt"
                  rules={{ required: " Product Type is required" }}
                  render={({ field, fieldState }) => (
                    <Fragment>
                      <Input
                        {...field}
                        type="select"
                        id="pt"
                        invalid={!!fieldState?.error}
                      >
                        <option value=""> Select</option>
                        {productTypeArr}
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
                <Label className="form-label" for="material">
                  Material
                </Label>
                <Controller
                  control={control}
                  name="material"
                  rules={{ required: "Material is required" }}
                  render={({ field, fieldState }) => (
                    <Fragment>
                      <Input
                        {...field}
                        type="select"
                        id="material"
                        invalid={!!fieldState?.error}
                      >
                        <option value=""> Select</option>
                        {materialArr}
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

              <Col xs={12} className="text-center mt-2 pt-50">
                <Button type="submit" className="me-1" color="primary">
                  Submit
                </Button>
                <Button
                  type="reset"
                  color="secondary"
                  outline
                  onClick={() => setShow(false)}
                >
                  Discard
                </Button>
              </Col>
            </Row>
          </Form>
        </ModalBody>
      </Modal>
    </Fragment>
  );
};

export default addEditMaster;
