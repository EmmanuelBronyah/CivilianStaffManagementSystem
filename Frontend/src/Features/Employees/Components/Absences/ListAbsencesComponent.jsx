import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import AbsencesData from "./AbsencesDataComponent";
import { useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function ListAbsences() {
  const [loading, setLoading] = useState(true);
  const { theme } = useTheme();
  const { setResponse } = useOutletContext();
  const navigate = useNavigate();
  const { serviceId } = useParams();

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
              className={style.addOccurrence}
              onClick={() =>
                navigate(`/home/employees/${serviceId}/absences/add`)
              }
            >
              Add Absences
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
                  <th title="Absences">Absences</th>
                  <th title="Start Date">Start Date</th>
                  <th title="End Date">End Date</th>
                  <th title="Authority">Authority</th>
                  <th title="Date">Date</th>
                </tr>
              </thead>
            )}

            <tbody>
              <AbsencesData
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
