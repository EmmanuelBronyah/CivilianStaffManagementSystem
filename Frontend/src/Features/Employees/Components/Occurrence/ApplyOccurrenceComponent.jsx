import style from "../../../../styles/components/applyoccurrencecomponent.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useOutletContext } from "react-router-dom";
import EmployeeInfo from "./EmployeeInfo";

export default function ApplyOccurrence() {
  const { theme } = useTheme();
  const { searchResults } = useOutletContext();

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
          {searchResults.length !== 0 ? (
            searchResults.map(({ service_id, last_name, other_names }) => (
              <EmployeeInfo
                serviceId={service_id}
                lastName={last_name}
                otherNames={other_names}
              />
            ))
          ) : (
            <div className={style.nothing}>
              <p>Nothing to show</p>
            </div>
          )}
        </div>
        <hr className={style.separator} />
        <div className={style.selectedEmployeesContainer}>
          <div className={style.selectedEmployeesTitle}>
            <p>Selected Employees</p>
          </div>
        </div>
      </div>
    </div>
  );
}
