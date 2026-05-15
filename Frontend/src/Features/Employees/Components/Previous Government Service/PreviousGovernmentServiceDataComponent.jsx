import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function PreviousGovernmentServiceData(props) {
  const [previousGovernmentServiceData, setPreviousGovernmentServiceData] =
    useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPreviousGovernmentServiceData = async () => {
      try {
        const res = await api.get(
          `api/previous-government-service/${serviceId}/employee/`,
        );
        setPreviousGovernmentServiceData(res.data);
        props.setLoading(false);
      } catch (error) {
        if (error.response.status === 404) {
          props.setLoading(false);
          return;
        }
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchPreviousGovernmentServiceData();
  }, []);

  const data = previousGovernmentServiceData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(
            `/home/employees/${serviceId}/previousGovernmentService/edit/${data.id}`,
          )
        }
      >
        <td title={data.institution}>{data.institution}</td>
        <td title={data.duration}>{data.duration}</td>
        <td title={data.position}>{data.position}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
