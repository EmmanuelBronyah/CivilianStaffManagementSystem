import style from "../../../../styles/components/applyoccurrencecomponent.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import { useOutletContext } from "react-router-dom";
import EmployeeInfo from "./EmployeeInfo";
import { MdArrowBackIos, MdArrowForwardIos } from "react-icons/md";
import ClipLoader from "react-spinners/ClipLoader";
import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import api from "../../../../api";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";

export default function ApplyOccurrence() {
  const { theme } = useTheme();

  const [searchParams, setSearchParams] = useSearchParams();
  const { setResponse } = useOutletContext();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [occurrenceLoading, setOccurrenceLoading] = useState(false);
  const [selectedEmployees, setSelectedEmployees] = useState(() => {
    const storedEmployees = localStorage.getItem("selectedEmployees");
    return storedEmployees ? JSON.parse(storedEmployees) : [];
  });
  const navigate = useNavigate();

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

  const applyOccurrence = async () => {
    setOccurrenceLoading(true);
    const formData = JSON.parse(localStorage.getItem("occurrenceData"));
    const occurrences = selectedEmployees.map(({ serviceId }) => ({
      employee: serviceId,
      grade: formData.grade.value,
      authority: formData.authority,
      level_step: formData.levelStep.value,
      monthly_salary: formData.monthlySalary,
      annual_salary: formData.annualSalary,
      event: formData.event.value,
      percentage_adjustment: formData?.percentageAdjustment?.label || null,
      wef_date: formData.wefDate || null,
      reason: formData.reason,
    }));

    try {
      const res = await api.post("api/occurrence/create/", occurrences);
      if (res.status === 201) {
        setResponse({
          message: `Updated Occurrences for ${selectedEmployees.length} employee record${selectedEmployees.length !== 1 ? "s" : ""}`,
          id: Date.now(),
        });

        localStorage.removeItem("occurrenceData");
        localStorage.removeItem("selectedEmployees");

        setTimeout(() => {
          navigate("/home/employees/form/occurrence");
        }, 3000);
      }
      setOccurrenceLoading(false);
    } catch (error) {
      setOccurrenceLoading(false);
      setResponse({
        message: getResponseMessages(error.response),
        type: "error",
        id: Date.now(),
      });

      localStorage.removeItem("occurrenceData");
      setTimeout(() => {
        navigate("/home/employees/form/occurrence");
      }, 3800);
    }
  };

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
      <div className={style.applyOccurrenceTitleAndButton}>
        <div className={style.applyOccurrenceTitle}>
          <p>Apply Occurrence</p>
        </div>
        {selectedEmployees.length > 0 && (
          <div className={style.applyOccurrenceButton}>
            <button onClick={applyOccurrence} disabled={occurrenceLoading}>
              {occurrenceLoading ? (
                <ClipLoader
                  size={13}
                  color={`${!theme ? "#1e1e1e" : "#d7fdd7"}`}
                />
              ) : (
                "Apply Occurrence"
              )}
            </button>
          </div>
        )}
      </div>

      <div className={style.twoSectionContainers}>
        <div className={style.searchResultsContainer}>
          <div className={style.searchResultsTitle}>
            <p>Search Results</p>
          </div>
          <div
            className={`${style.resultsCount} ${results.results?.length > 0 && style.displayBlock}`}
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
                occurrenceLoading={occurrenceLoading}
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
            <button disabled={!results.previous || occurrenceLoading}>
              <MdArrowBackIos
                title="Previous"
                className={style.navigateIcons}
                onClick={goToPreviousPage}
              />
            </button>

            <button disabled={!results.next || occurrenceLoading}>
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
                occurrenceLoading={occurrenceLoading}
                showSelectedEmployees={true}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
