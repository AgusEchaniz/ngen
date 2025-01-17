import React from "react";
import { Button, Modal } from "react-bootstrap";
import ReadEvent from "./ReadEvent";
import "./ModalReadEvent.css";

const ModalReadEvent = ({ modalShowCase, returnToListOfCases, linkCaseToEvent, tableDetail, closeModalDetail, url }) => {
  return (
    <Modal
      show={modalShowCase}
      size="lg"
      onHide={tableDetail ? closeModalDetail : returnToListOfCases}
      aria-labelledby="contained-modal-title-vcenter"
      centered
      dialogClassName="modal-90w"
    >
      <Modal.Header closeButton />
      <Modal.Body>
        <div id="example-collapse-text">
          <ReadEvent url={url} />
        </div>
      </Modal.Body>
      {tableDetail ? (
        ""
      ) : (
        <Modal.Footer>
          <Button variant="outline-primary" onClick={linkCaseToEvent}>
            Vincular
          </Button>
          <Button variant="outline-secondary" onClick={returnToListOfCases}>
            Volver al listado
          </Button>
        </Modal.Footer>
      )}
    </Modal>
  );
};

export default ModalReadEvent;
