import { useNavigate, useParams } from "react-router-dom";
import BaseSkeleton from "../../../../Components/Common/SkeletonComponent";
import api from "../../../../api";
import getResponseMessages from "../../../../utils/extractResponseMessage";
import { useEffect, useState } from "react";

export default function SpouseData(props) {
  const [spouseData, setSpouseData] = useState([]);
  const { serviceId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSpouseData = async () => {
      try {
        const res = await api.get(`api/marriage/${serviceId}/employee/`);
        setSpouseData(res.data);
        props.setLoading(false);
      } catch (error) {
        props.setResponse({
          message: getResponseMessages(error.response),
          type: "error",
          id: Date.now(),
        });
      }
    };
    fetchSpouseData();
  }, []);

  const data = spouseData.map((data) => {
    return (
      <tr
        key={data.id}
        onClick={() =>
          navigate(`/home/employees/${serviceId}/spouse/edit/${data.id}`)
        }
      >
        <td title={data.spouse_name}>{data.spouse_name}</td>
        <td title={data.phone_number}>{data.phone_number}</td>
        <td title={data.address}>{data.address}</td>
        <td title={data.registration_number}>{data.registration_number}</td>
        <td title={data.marriage_date}>{data.marriage_date}</td>
        <td title={data.marriage_place}>{data.marriage_place}</td>
      </tr>
    );
  });

  if (props.loading) {
    return <BaseSkeleton width="100%" height="100vh" />;
  } else {
    return data;
  }
}
