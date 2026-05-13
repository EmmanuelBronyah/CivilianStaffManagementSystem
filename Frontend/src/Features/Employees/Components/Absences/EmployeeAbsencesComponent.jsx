import { Outlet, useOutletContext } from "react-router-dom";

export default function EmployeeAbsences() {
  const { setResponse } = useOutletContext();

  return <Outlet context={{ setResponse }} />;
}
