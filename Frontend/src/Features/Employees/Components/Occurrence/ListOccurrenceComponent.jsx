import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import OccurrenceData from "./OccurrenceDataComponent";
import { useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import useFetchUserRole from "../../../hooks/fetchUserRoleHook";
import { useEffect } from "react";

export default function ListOccurrence() {
  const [loading, setLoading] = useState(true);
  const { theme } = useTheme();
  const { setResponse } = useOutletContext();
  const navigate = useNavigate();
  const { serviceId } = useParams();
  const { role, response } = useFetchUserRole();

  useEffect(() => {
    if (!response) return;
    setResponse(response);
  });

  return (
    <div
      className={`${style.listEmployeeOccurrence} ${!theme ? style.dark : ""}`}
    >
      <div className={style.occurrencePageButtonAndTableContainer}>
        <div className={style.addOccurrenceButtonContainer}>
          {loading ? (
            <BaseSkeleton width={170} height={39} />
          ) : (
            <button
              className={`${style.addOccurrence} ${!role || role === "VIEWER" ? style.displayNone : ""}`}
              onClick={() =>
                navigate(`/home/employees/${serviceId}/occurrence/add`)
              }
            >
              Add Occurrence
            </button>
          )}
        </div>

        <div>
          <table>
            {loading ? (
              <BaseSkeleton height={38} />
            ) : (
              <thead>
                <tr>
                  <th title="Service Number">Service Number</th>
                  <th title="Grade">Grade</th>
                  <th title="Authority">Authority</th>
                  <th title="LevStep">LevStep</th>
                  <th title="Monthly Salary">Monthly Salary</th>
                  <th title="Annual Salary">Annual Salary</th>
                  <th title="WEF Date">WEF Date</th>
                  <th title="Date">Date</th>
                  <th title="Reason">Reason</th>
                </tr>
              </thead>
            )}

            <tbody>
              <OccurrenceData
                setResponse={setResponse}
                loading={loading}
                setLoading={setLoading}
              />
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
