import { useRef, useState } from "react";
import ListEmployeeOccurrence from "./ListEmployeeOccurrenceComponent";
import EditEmployeeOccurrence from "./EditEmployeeOccurrenceComponent";

export default function EmployeeOccurrence(props) {
  const [currentOccurrencePage, setCurrentOccurrencePage] =
    useState("List Occurrence");
  const occurrenceId = useRef("");

  const editOccurrence = (id) => {
    occurrenceId.current = id;
    setCurrentOccurrencePage("Edit Occurrence");
  };

  return (
    <>
      {currentOccurrencePage === "List Occurrence" && (
        <ListEmployeeOccurrence
          serviceId={props.serviceId}
          setResponse={props.setResponse}
          editOccurrence={editOccurrence}
        />
      )}
      {currentOccurrencePage === "Edit Occurrence" && (
        <EditEmployeeOccurrence
          occurrenceId={occurrenceId.current}
          setResponse={props.setResponse}
          setCurrentOccurrencePage={setCurrentOccurrencePage}
        />
      )}
    </>
  );
}
