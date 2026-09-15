import style from "../../../../styles/components/advancedsearch.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useEffect, useState } from "react";
import { MdArrowBackIos, MdArrowForwardIos } from "react-icons/md";
import { components } from "./constants";

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
          },
          {
            name: "Occurrence",
            active: false,
          },
          {
            name: "Children",
            active: false,
          },
          {
            name: "Course",
            active: false,
          },
          {
            name: "Identity",
            active: false,
          },
          {
            name: "Spouse",
            active: false,
          },
          {
            name: "Emergency | Next of Kin",
            active: false,
          },
          {
            name: "Previous Government Service",
            active: false,
          },
          {
            name: "Service With Forces",
            active: false,
          },
          {
            name: "Termination of Appointment",
            active: false,
          },
        ];
  });
  const [currentIndex, setCurrentIndex] = useState(0);
  const [formData, setFormData] = useState({});

  // Names of buttons with a `true` active status
  const selectedButtons = buttons
    .filter((button) => button.active)
    .map((button) => button.name);

  const CurrentComponent = components[selectedButtons[currentIndex]];

  // Save buttons in localstorage every time `buttons` changes
  useEffect(() => {
    localStorage.setItem("buttons", JSON.stringify(buttons));
  }, [buttons]);

  useEffect(() => {
    if (currentIndex >= selectedButtons.length) {
      setCurrentIndex(Math.max(selectedButtons.length - 1, 0));
    }
  }, [selectedButtons, currentIndex]);

  const toggleActiveStatus = (buttonText) => {
    setButtons((prev) =>
      prev.map((button) =>
        button.name === buttonText
          ? { ...button, active: !button.active }
          : button,
      ),
    );
  };

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

  useEffect(() => {
    console.log("formdata -> ", formData);
  }, [formData]);

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
          <div className={style.recordButtonsContainer}>
            {buttons.map(({ name, active }) => (
              <button
                key={name}
                className={active ? style.recordButtonActive : ""}
                onClick={() => toggleActiveStatus(name)}
              >
                {name}
              </button>
            ))}
          </div>
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
                {CurrentComponent && (
                  <CurrentComponent
                    formData={formData}
                    setFormData={setFormData}
                  />
                )}
                <div
                  className={`${style.navigateButtonsContainer} ${selectedButtons.length >= 1 ? "" : style.displayNone}`}
                >
                  <button
                    disabled={currentIndex === 0}
                    onClick={goToPreviousPage}
                  >
                    <MdArrowBackIos
                      title="Previous"
                      className={style.navigateIcons}
                    />
                  </button>
                  <button
                    disabled={currentIndex === selectedButtons.length - 1}
                    onClick={goToNextPage}
                  >
                    <MdArrowForwardIos
                      title="Next"
                      className={style.navigateIcons}
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
