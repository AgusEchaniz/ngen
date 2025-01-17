import React, { useEffect, useState } from "react";
import { Button, Card, Col, Form, Row } from "react-bootstrap";
import { validateDescription, validateName, validateType, validateUnrequiredInput } from "../../utils/validators/taxonomy";
import { getMinifiedTaxonomy, postTaxonomy } from "../../api/services/taxonomies";
import SelectLabel from "../../components/Select/SelectLabel";
import { useTranslation } from "react-i18next";
import { getMinifiedTaxonomyGroups } from "../../api/services/taxonomyGroups";
import DropdownState from "../../components/Dropdown/DropdownState";
import CrudButton from "components/Button/CrudButton";

const CreateTaxonomy = () => {
  const [type, setType] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [parent, setParent] = useState("");
  const [alias_of, setAlias_of] = useState("");
  const [group, setGroup] = useState("");
  const [showAlert, setShowAlert] = useState(false);
  const [active, setActive] = useState(true);
  const [needs_review, setNeeds_review] = useState(false);

  const [taxonomies, setTaxonomies] = useState([]);
  const [taxonomyGroups, setTaxonomyGroups] = useState([]);

  const [selectTaxonomyParent, setSelectTaxonomyParent] = useState();
  const [selectGroup, setSelectGroup] = useState("");
  const [selectTaxonomyAlias_of, setSelectTaxonomyAlias_of] = useState();
  const [selectedType, setSelectedType] = useState();
  const [isGroupDisabled, setIsGroupDisabled] = useState(false);

  const { t } = useTranslation();

  useEffect(() => {
    getMinifiedTaxonomy().then((response) => {
      let listTaxonomies = response.map((taxonomy) => {
        return { value: taxonomy.url, label: taxonomy.name };
      });
      setTaxonomies(listTaxonomies);
    });

    getMinifiedTaxonomyGroups().then((response) => {
      let listTaxonomyGroups = response.map((taxonomyGroup) => {
        return { value: taxonomyGroup.url, label: taxonomyGroup.name };
      });
      setTaxonomyGroups(listTaxonomyGroups);
    });

    const handleResize = (e) => {
      e.preventDefault(); // Detiene el comportamiento predeterminado del evento de redimensionamiento
      // Tu lógica de manejo de redimensionamiento aquí (si es necesario)
    };

    // Agrega un listener de redimensionamiento cuando el componente se monta
    window.addEventListener("resize", handleResize);

    // Elimina el listener cuando el componente se desmonta
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const handleParentChange = (value) => {
    setParent(value);
    setGroup(null);
    setSelectGroup(null);
    if (value) {
      setIsGroupDisabled(true);
    } else {
      setIsGroupDisabled(false);
    }
  };

  const createTaxonomy = () => {
    postTaxonomy(type, name, description, active, parent, alias_of, needs_review, group)
      .then(() => {
        window.location.href = "/taxonomies";
      })
      .catch((error) => {
        console.log(error);
        setShowAlert(true);
      });
  };

  const resetShowAlert = () => {
    setShowAlert(false);
  };

  let typeOption = [
    {
      value: "vulnerability",
      label: t("ngen.vulnerability")
    },
    {
      value: "incident",
      label: t("ngen.incident")
    },
    {
      value: "other",
      label: t("ngen.other")
    }
  ];

  return (
    <React.Fragment>
      <Row>
        <Col sm={12}>
          <Card>
            <Card.Header>
              <Card.Title as="h5">{t("ngen.taxonomy_one")}</Card.Title>
            </Card.Header>
            <Card.Body>
              <Form>
                <Row>
                  <Col sm={12} lg={6}>
                    <Form.Group>
                      <Form.Label>
                        {t("ngen.name_one")} <b style={{ color: "red" }}>*</b>
                      </Form.Label>
                      <Form.Control
                        type="text"
                        placeholder={t("ngen.name_one")}
                        onChange={(e) => setName(e.target.value)}
                        isInvalid={!validateName(name)}
                      />
                      {validateName(name) ? "" : <div className="invalid-feedback">{t("ngen.name.invalid")}</div>}
                    </Form.Group>
                  </Col>
                  <Col sm={12} lg={4}>
                    <SelectLabel
                      set={setType}
                      setSelect={setSelectedType}
                      options={typeOption}
                      value={selectedType}
                      placeholder={t("ngen.type")}
                      required={true}
                    />
                  </Col>
                  <Col sm={12} lg={1}>
                    <Form.Group>
                      <Form.Label>{t("ngen.state_one")}</Form.Label>
                      <DropdownState state={true} setActive={setActive}></DropdownState>
                    </Form.Group>
                  </Col>
                  <Col sm={12} lg={1}>
                    <Form.Group>
                      <Form.Label>{t("ngen.taxonomy.needs_review")}</Form.Label>
                      <DropdownState state={false} setActive={setNeeds_review} str_true="w.yes" str_false="w.no" />
                    </Form.Group>
                  </Col>
                </Row>
                <Row>
                  <Col sm={12} lg={4}>
                    <SelectLabel
                      set={handleParentChange}
                      setSelect={setSelectTaxonomyParent}
                      options={taxonomies}
                      value={selectTaxonomyParent}
                      placeholder={t("ngen.taxonomy.parent")}
                      legend={t("ngen.taxonomy.parent.legend.create")}
                    />
                  </Col>
                  <Col sm={12} lg={4}>
                    <SelectLabel
                      set={setGroup}
                      setSelect={setSelectGroup}
                      options={taxonomyGroups}
                      value={selectGroup}
                      placeholder={t("ngen.taxonomy.group")}
                      disabled={isGroupDisabled}
                      legend={t("ngen.taxonomy.group.legend.create")}
                    />
                  </Col>
                  <Col sm={12} lg={4}>
                    <SelectLabel
                      set={setAlias_of}
                      setSelect={setSelectTaxonomyAlias_of}
                      options={taxonomies}
                      value={selectTaxonomyAlias_of}
                      placeholder={t("ngen.taxonomy.alias_of")}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col sm={12} lg={12}>
                    <Form.Group>
                      <Form.Label>{t("ngen.description")}</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={3}
                        placeholder={t("ngen.description")}
                        onChange={(e) => setDescription(e.target.value)}
                        isInvalid={validateUnrequiredInput(description) ? !validateDescription(description) : false}
                      />
                      {validateDescription(description) ? "" : <div className="invalid-feedback">{t("w.validateDesc")}</div>}
                    </Form.Group>
                  </Col>
                </Row>
                <Form.Group as={Col}>
                  {validateType(type) && validateName(name) && name !== "" ? (
                    <Button variant="primary" onClick={createTaxonomy}>
                      {t("button.save")}
                    </Button>
                  ) : (
                    <Button variant="primary" disabled>
                      {t("button.save")}
                    </Button>
                  )}
                  <CrudButton type="cancel" />
                </Form.Group>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </React.Fragment>
  );
};

export default CreateTaxonomy;
