import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function NextOfKinData(props) {
  const [nextOfKinData, setNextOfKinData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchNextOfKinData = async () => {
      try {
        const res = await api.get(`api/next-of-kin/${serviceId}/employee/`);
        setNextOfKinData(res.data);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchNextOfKinData();
  }, []);

  const data = nextOfKinData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/nextOfKin/edit/${data.id}`)
        }
      >
        <td title={data.name}>{data.name}</td>
        <td title={data.relation}>{data.relation}</td>
        <td title={data.next_of_kin_email}>{data.next_of_kin_email}</td>
        <td title={data.address}>{data.address}</td>
        <td title={data.phone_number}>{data.phone_number}</td>
        <td title={data.emergency_contact}>{data.emergency_contact}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
