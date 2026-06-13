import style from "../../../../styles/components/advancedsearch.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useState } from "react";

export default function AdvancedSearch() {
  const { theme } = useTheme();

  const [buttons, setButtons] = useState([
    { name: "Employee", active: false },
    { name: "Occurrence", active: false },
    { name: "Children", active: false },
    { name: "Course", active: false },
    { name: "Identity", active: false },
    { name: "Spouse", active: false },
    { name: "Emergency | Next of Kin", active: false },
    { name: "Previous Government Service", active: false },
    { name: "Service With Forces", active: false },
    { name: "Termination of Appointment", active: false },
  ]);

  const toggleActiveStatus = (buttonText) => {
    setButtons((prev) =>
      prev.map((buttonObj) =>
        buttonObj.name === buttonText
          ? { ...buttonObj, active: !buttonObj.active }
          : { ...buttonObj },
      ),
    );
  };

  const recordButtons = buttons.map(({ name, active }) => (
    <button
      key={name}
      className={active ? style.recordButtonActive : ""}
      onClick={() => toggleActiveStatus(name)}
    >
      {name}
    </button>
  ));

  return (
    <div className={`${style.advancedSearch} ${!theme ? style.dark : ""}`}>
      <div className={style.advancedSearchTitleAndInfo}>
        <p>Advanced Search</p>
        <i className={style.info}>
          Search employees by their fields or refine results using related
          records like absences, occurrences, courses and more
        </i>
      </div>
      <div className={style.searchMainArea}>
        <div className={style.selectRecordsContainer}>
          <div className={style.selectRecordsText}>
            <i>Select Records</i>
          </div>
          <div className={style.recordButtonsContainer}>{recordButtons}</div>
        </div>
      </div>
    </div>
  );
}
