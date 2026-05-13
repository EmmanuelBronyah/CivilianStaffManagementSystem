import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function OccurrenceData(props) {
  const [occurrenceData, setOccurrenceData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOccurrenceData = async () => {
      try {
        const res = await api.get(`api/occurrence/${serviceId}/employee/`);
        setOccurrenceData(res.data);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
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
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/occurrence/edit/${data.id}`)
        }
      >
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

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
