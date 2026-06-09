import style from "../../../../styles/components/applyoccurrencecomponent.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useOutletContext } from "react-router-dom";
import EmployeeInfo from "./EmployeeInfo";
import { MdArrowBackIos, MdArrowForwardIos } from "react-icons/md";
import ClipLoader from "react-spinners/ClipLoader";
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import api from "../../../../api";

export default function ApplyOccurrence() {
  const { theme } = useTheme();

  const [searchParams, setSearchParams] = useSearchParams();
  const { setResponse } = useOutletContext();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedEmployees, setSelectedEmployees] = useState(() => {
    const storedEmployees = localStorage.getItem("selectedEmployees");
    return storedEmployees ? JSON.parse(storedEmployees) : [];
  });

  const page = searchParams.get("page") || 1;
  const query = searchParams.get("q") || "";

  useEffect(() => {
    setLoading(true);

    const searchEmployee = async () => {
      try {
        const res = await api.get(`api/employees/staff/search/`, {
          params: { page: page, query: query },
        });
        setLoading(false);

        setResults(res.data);
      } catch (error) {
        setLoading(false);
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };

    searchEmployee();
  }, [query, page]);

  useEffect(() => {
    localStorage.setItem(
      "selectedEmployees",
      JSON.stringify(selectedEmployees),
    );
  }, [selectedEmployees]);

  const toggleEmployee = (employee) => {
    setSelectedEmployees((prev) => {
      const exists = prev.some((item) => item.serviceId === employee.serviceId);
      if (exists) {
        return prev.filter((item) => item.serviceId !== employee.serviceId);
      }
      return [...prev, employee];
    });
  };

  const goToNextPage = () => {
    setSearchParams({
      q: query,
      page: Number(page) + 1,
    });
  };

  const goToPreviousPage = () => {
    setSearchParams({
      q: query,
      page: Math.max(Number(page) - 1, 1),
    });
  };

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
          <div
            className={`${style.resultsCount} ${results.results?.length === 0 && style.displayNone}`}
          >
            <p>
              <i>{results.count || ""}</i> record
              {results.count === 1 ? "" : "s"}
            </p>
          </div>
          {loading ? (
            <ClipLoader
              className={style.loadingSpinner}
              size={30}
              color={`${!theme ? "#808080" : "#004700"}`}
            />
          ) : results.results?.length !== 0 ? (
            results.results?.map(({ service_id, last_name, other_names }) => (
              <EmployeeInfo
                key={service_id}
                serviceId={service_id}
                lastName={last_name}
                otherNames={other_names}
                onToggle={() =>
                  toggleEmployee({
                    serviceId: service_id,
                    lastName: last_name,
                    otherNames: other_names,
                  })
                }
                checked={selectedEmployees.some(
                  (employee) => service_id === employee.serviceId,
                )}
              />
            ))
          ) : (
            <div className={style.nothing}>
              <p>Nothing to show</p>
            </div>
          )}
          <div
            className={`${style.navigateButtonsContainer} ${results.results?.length === 0 && style.displayNone}`}
          >
            <button disabled={!results.previous}>
              <MdArrowBackIos
                title="Previous"
                className={style.navigateIcons}
                onClick={goToPreviousPage}
              />
            </button>

            <button disabled={!results.next}>
              <MdArrowForwardIos
                title="Next"
                className={style.navigateIcons}
                onClick={goToNextPage}
              />
            </button>
          </div>
        </div>
        <hr className={style.separator} />
        <div
          className={`${style.selectedEmployeesContainer} ${selectedEmployees.length >= 20 ? style.overflow : ""}`}
        >
          <div className={style.selectedEmployeesTitle}>
            <p>Selected Employees</p>
          </div>
          <div
            className={`${style.resultsCount} ${selectedEmployees.length === 0 && style.displayNone}`}
          >
            <p>
              <i>{selectedEmployees.length || ""}</i> record
              {selectedEmployees.length === 1 ? "" : "s"}
            </p>
          </div>
          <div>
            {selectedEmployees.map(({ serviceId, lastName, otherNames }) => (
              <EmployeeInfo
                key={serviceId}
                serviceId={serviceId}
                lastName={lastName}
                otherNames={otherNames}
                showSelectedEmployees={true}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
