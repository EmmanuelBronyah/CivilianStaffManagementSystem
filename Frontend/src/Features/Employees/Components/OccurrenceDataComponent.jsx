import style from "../../../styles/components/employees.module.css";
import { useTheme } from "../../../context/ThemeContext";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function OccurrenceData({
  serviceId,
  setResponse,
  editOccurrence,
}) {
  const [occurrenceData, setOccurrenceData] = useState([]);

  useEffect(() => {
    const fetchOccurrenceData = async () => {
      try {
        const res = await api.get(`api/occurrence/${serviceId}/employee/`);
        setOccurrenceData(res.data);
      } catch (error) {
        setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchOccurrenceData();
  }, []);

  const data = occurrenceData.map((data) => {
    return (
      <tr key={data.id} onClick={() => editOccurrence(data.id)}>
        <td title={data.service_id}>{data.service_id}</td>
        <td title={data.grade_display}>{data.grade_display}</td>
        <td title={data.authority}>{data.authority}</td>
        <td title={data.level_step_display}>{data.level_step_display}</td>
        <td title={data.monthly_salary}>{data.monthly_salary}</td>
        <td title={data.annual_salary}>{data.annual_salary}</td>
        <td title={data.event_display}>{data.event_display}</td>
        <td title={data.wef_date}>{data.wef_date}</td>
        <td title={data.reason}>{data.reason}</td>
      </tr>
    );
  });

  return data;
}
