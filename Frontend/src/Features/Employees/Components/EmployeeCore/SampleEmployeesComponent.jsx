import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import EmployeeData from "./EmployeeDataComponent";
import { useState } from "react";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import { useOutletContext } from "react-router-dom";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function SampleEmployees() {
  const [loading, setLoading] = useState(true);
  const { setResponse } = useOutletContext();
  const { role, response } = useFetchUserRole();
  const navigate = useNavigate();

  const { theme } = useTheme();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  return (
    <>
      <div
        className={`${style.listEmployeesContainer} ${!theme ? style.dark : ""}`}
      >
        <div className={style.titleAndButtonsContainer}>
          <div className={style.employeeTitleAndTwoButtonsContainer}>
            {loading ? (
              <BaseSkeleton width={200} height={34} />
            ) : (
              <p className={style.employeesTitle}>Sample Employees</p>
            )}

            <div
              className={`${style.twoButtonsContainer} ${!role || (role === "VIEWER" && style.displayNone)}`}
            >
              {loading ? (
                <BaseSkeleton width={120} height={36} />
              ) : (
                <button
                  className={style.newEmployeeButton}
                  onClick={() => navigate("/home/employees/add")}
                >
                  New Employee
                </button>
              )}

              {loading ? (
                <BaseSkeleton width={120} height={36} />
              ) : (
                <button className={style.advancedSearchButton}>
                  Advanced Search
                </button>
              )}
            </div>
          </div>
          {loading ? (
            <BaseSkeleton width={150} height={36} />
          ) : (
            <button
              className={`${style.applyOccurrenceButton} ${!role || (role === "VIEWER" && style.displayNone)}`}
              onClick={() => navigate("/home/employees/form/occurrence/")}
            >
              Apply Occurrence
            </button>
          )}
        </div>

        <div className={style.employeeListContainer}>
          <table>
            {loading ? (
              <BaseSkeleton height={38} />
            ) : (
              <thead>
                <tr>
                  <th title="Service Number">Service Number</th>
                  <th title="Name">Name</th>
                  <th title="Unit">Unit</th>
                  <th title="Grade">Grade</th>
                  <th title="Category">Category</th>
                  <th title="Appointment Date">Appointment Date</th>
                  <th title="Status">Status</th>
                </tr>
              </thead>
            )}
            <tbody>
              <EmployeeData
                loading={loading}
                setLoading={setLoading}
                setResponse={setResponse}
              />
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
