import style from "../../../../styles/components/advancedsearch.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useEffect, useState } from "react";
import Dropdown from "./Dropdown";
import { MdArrowBackIos, MdArrowForwardIos } from "react-icons/md";
import EmployeeInput from "./EmployeeInput/EmployeeInput";
import OccurrenceInput from "./OccurrenceInput/OccurrenceInput";
import ChildrenInput from "./ChildrenInput/ChildrenInput";
import SpouseInput from "./SpouseInput/SpouseInput";
import CourseInput from "./CourseInput/CourseInput";
import IdentityInput from "./IdentityInput/IdentityInput";
import NextOfKinInput from "./NextOfKinInput/NextOfKinInput";
import PreviousGovernmentServiceInput from "./PreviousGovernmentServiceInput/PreviousGovernmentServiceInput";
import ServiceWithForcesInput from "./ServiceWithForcesInput/ServiceWithForcesInput";
import TerminationOfAppointmentInput from "./TerminationOfAppointmentInput/TerminationOfAppointmentInput ";

export default function AdvancedSearch() {
  const { theme } = useTheme();
  const [buttons, setButtons] = useState(() => {
    const storedButtons = localStorage.getItem("buttons");
    return storedButtons
      ? JSON.parse(storedButtons)
      : [
          {
            name: "Employee",
            active: false,
            link: "/home/employees/advanced-search/employee",
          },
          {
            name: "Occurrence",
            active: false,
            link: "/home/employees/advanced-search/occurrence",
          },
          {
            name: "Children",
            active: false,
            link: "/home/employees/advanced-search/children",
          },
          {
            name: "Course",
            active: false,
            link: "/home/employees/advanced-search/course",
          },
          {
            name: "Identity",
            active: false,
            link: "/home/employees/advanced-search/identity",
          },
          {
            name: "Spouse",
            active: false,
            link: "/home/employees/advanced-search/spouse",
          },
          {
            name: "Emergency | Next of Kin",
            active: false,
            link: "/home/employees/advanced-search/emergency-next-of-kin",
          },
          {
            name: "Previous Government Service",
            active: false,
            link: "/home/employees/advanced-search/previous-government-service",
          },
          {
            name: "Service With Forces",
            active: false,
            link: "/home/employees/advanced-search/service-with-forces",
          },
          {
            name: "Termination of Appointment",
            active: false,
            link: "/home/employees/advanced-search/termination-of-appointment",
          },
        ];
  });
  const [selectedButtons, setSelectedButtons] = useState(() => {
    const storedButtons = localStorage.getItem("selectedButtons");
    return storedButtons ? JSON.parse(storedButtons) : [];
  });
  const [currentIndex, setCurrentIndex] = useState(0);
  const [dropdownData, setDropdownData] = useState({});

  // Save buttons in localstorage every time `buttons` changes
  useEffect(() => {
    localStorage.setItem("buttons", JSON.stringify(buttons));
  }, [buttons]);

  // Get selected buttons names in local storage
  useEffect(() => {
    const activeButtons = buttons.filter((button) => button.active === true);
    const buttonNames = activeButtons.map(({ name }) => name);
    setSelectedButtons(buttonNames);
    localStorage.setItem("selectedButtons", JSON.stringify(buttonNames));
  }, [buttons]);

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

  const goToNextPage = () => {
    if (currentIndex < selectedButtons.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const goToPreviousPage = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

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
        <div className={style.recordInputAndFiltersContainer}>
          <div className={style.recordInputContainer}>
            <div className={style.fillFiltersTitle}>
              <p>Fill filters for chosen records </p>
            </div>
            {selectedButtons.length === 0 ? (
              <div className={style.nothingToShow}>
                <p>Nothing to show</p>
              </div>
            ) : (
              <div className={style.selectDataContainer}>
                {selectedButtons[currentIndex] === "Employee" && (
                  <EmployeeInput setDropdownData={setDropdownData} />
                )}
                {selectedButtons[currentIndex] === "Occurrence" && (
                  <OccurrenceInput />
                )}
                {selectedButtons[currentIndex] === "Children" && (
                  <ChildrenInput />
                )}
                {selectedButtons[currentIndex] === "Spouse" && <SpouseInput />}
                {selectedButtons[currentIndex] === "Course" && <CourseInput />}
                {selectedButtons[currentIndex] === "Identity" && (
                  <IdentityInput />
                )}
                {selectedButtons[currentIndex] ===
                  "Emergency | Next of Kin" && <NextOfKinInput />}
                {selectedButtons[currentIndex] ===
                  "Previous Government Service" && (
                  <PreviousGovernmentServiceInput />
                )}
                {selectedButtons[currentIndex] === "Service With Forces" && (
                  <ServiceWithForcesInput />
                )}
                {selectedButtons[currentIndex] ===
                  "Termination of Appointment" && (
                  <TerminationOfAppointmentInput />
                )}
                <div
                  className={`${style.navigateButtonsContainer} ${selectedButtons.length >= 1 ? "" : style.displayNone}`}
                >
                  <button disabled={currentIndex === 0}>
                    <MdArrowBackIos
                      title="Previous"
                      className={style.navigateIcons}
                      onClick={goToPreviousPage}
                    />
                  </button>
                  <button disabled={currentIndex == selectedButtons.length - 1}>
                    <MdArrowForwardIos
                      title="Next"
                      className={style.navigateIcons}
                      onClick={goToNextPage}
                    />
                  </button>
                </div>
              </div>
            )}
          </div>
          <hr />
          <div className={style.filtersContainer}>
            <div className={style.previewFiltersTitle}>
              <p>Preview Filters</p>
            </div>
            <div className={style.previewFilters}></div>
          </div>
        </div>
      </div>
    </div>
  );
}
