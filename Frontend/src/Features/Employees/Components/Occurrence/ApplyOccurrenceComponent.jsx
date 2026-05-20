import style from "../../../../styles/components/applyoccurrencecomponent.module.css";
import { useTheme } from "../../../../context/ThemeContext";

export default function ApplyOccurrence() {
  const { theme } = useTheme();

  return (
    <div
      className={`${style.applyOccurrenceContainer} ${!theme ? style.dark : ""}`}
    >
      <div className={style.applyOccurrenceTitle}>
        <p>Apply Occurrence</p>
      </div>
      <div className={style.twoSectionContainers}>
        <div className={style.searchResultsContainer}>
          <div className={style.searchResultsTitle}>
            <p>Search Results</p>
          </div>
        </div>
        <div className={style.selectedEmployeesContainer}>
          <div className={style.selectedEmployeesTitle}>
            <p>Selected Employees</p>
          </div>
        </div>
      </div>
    </div>
  );
}
