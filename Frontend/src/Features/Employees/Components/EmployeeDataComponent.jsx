import { useEffect, useState } from "react";
import api from "../../../api";
import getResponseMessages from "../../../utils/extractResponseMessage";
import BaseSkeleton from "../../../Components/Common/SkeletonComponent";

export default function EmployeeData(props) {
  const [employeeData, setEmployeeData] = useState([]);

  useEffect(() => {
    const fetchEmployeeData = async () => {
      try {
        const res = await api.get("api/employees/staff/dto/");
        props.setLoading(false);
        setEmployeeData(res.data.results);
      } catch (error) {
        props.setLoading(false);
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
        return;
      }
    };
    fetchEmployeeData();
  }, []);

  const data = employeeData.map((data) => {
    return (
      <tr
        key={data.service_id}
        onClick={() => props.displayEmployeeInfo(data.service_id)}
      >
        <td title={data.service_id}>{data.service_id}</td>
        <td title={`${data.last_name} ${data.other_names}`}>
          {data.last_name} {data.other_names}
        </td>
        <td title={data.unit}>{data.unit}</td>
        <td title={data.grade}>{data.grade}</td>
        <td title={data.category}>{data.category}</td>
        <td title={data.appointment_date}>{data.appointment_date}</td>
        <td title={data.termination_status}>{data.termination_status}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
