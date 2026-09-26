import style from "../../../../styles/components/advancedsearch.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useEffect, useState } from "react";
import { MdArrowBackIos, MdArrowForwardIos } from "react-icons/md";
import ParentInput from "./ParentInput";
import PreviewFilters from "./PreviewFilters";
import { BUTTON_STORAGE_KEY, FORMDATA_STORAGE_KEY } from "./constants";
import { validateFormData } from "../../utils/checkFormData";
import { useOutletContext } from "react-router-dom";

export default function AdvancedSearch() {
  const { theme } = useTheme();
  const [buttons, setButtons] = useState(() => {
    const storedButtons = localStorage.getItem(BUTTON_STORAGE_KEY);
    return storedButtons
      ? JSON.parse(storedButtons)
      : [
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
            name: "Employee",
            active: false,
          },
          {
            name: "Occurrence",
            active: false,
          },
          {
            name: "Termination of Appointment",
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
            name: "Absence",
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
        ];
  });
  const [currentIndex, setCurrentIndex] = useState(0);
  const [formData, setFormData] = useState(() => {
    const storedFormData = localStorage.getItem(FORMDATA_STORAGE_KEY);
    return storedFormData ? JSON.parse(storedFormData) : {};
  });
  const { setResponse } = useOutletContext();

  // Names of buttons with a `true` active status
  const selectedButtons = buttons
    .filter((button) => button.active)
    .map((button) => button.name);

  useEffect(() => {
    localStorage.setItem(FORMDATA_STORAGE_KEY, JSON.stringify(formData));
  }, [formData]);

  // Set buttons in localstorage on change and delete deselected record's data in formData
  useEffect(() => {
    localStorage.setItem(BUTTON_STORAGE_KEY, JSON.stringify(buttons));

    setFormData((prev) => {
      const activeButtons = buttons
        .filter(({ active }) => active)
        .map(({ name }) => name);

      return Object.fromEntries(
        Object.entries(prev).filter(([record]) =>
          activeButtons.includes(record),
        ),
      );
    });
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

  const performSearch = () => {
    const response = validateFormData(formData);
    if (response !== true) {
      setResponse({
        message: response,
        type: "error",
        id: Date.now(),
      });
      return;
    }
  };

  useEffect(() => {
    console.log("formdata -> ", formData);
  }, [formData]);

  return (
    <div className={`${style.advancedSearch} ${!theme ? style.dark : ""}`}>
      <div className={style.advancedSearchTitleAndInfo}>
        <div className={style.textSection}>
          <p>Advanced Search</p>
          <i className={style.info}>
            Search employees by their fields or refine results using related
            records like absences, occurrences, courses and more
          </i>
        </div>
        <div
          className={`${style.buttonSection} ${Object.keys(formData).length === 0 ? style.displayNone : ""}`}
        >
          <button onClick={performSearch}>Search</button>
        </div>
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
                <ParentInput
                  formData={formData}
                  setFormData={setFormData}
                  record={selectedButtons[currentIndex]}
                />
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
            <PreviewFilters formData={formData} />
          </div>
        </div>
      </div>
    </div>
  );
}
