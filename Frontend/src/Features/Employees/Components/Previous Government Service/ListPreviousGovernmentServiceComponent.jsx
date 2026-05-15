import style from "../../../../styles/components/employees.module.css";
import { useTheme } from "../../../../context/ThemeContext";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import PreviousGovernmentServiceData from "./PreviousGovernmentServiceDataComponent";
import { useState } from "react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";

export default function ListPreviousGovernmentService() {
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
                navigate(
                  `/home/employees/${serviceId}/previousGovernmentService/add`,
                )
              }
            >
              Add Service
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
                  <th title="Institution">Institution</th>
                  <th title="Duration">Duration</th>
                  <th title="Position">Position</th>
                </tr>
              </thead>
            )}

            <tbody>
              <PreviousGovernmentServiceData
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
