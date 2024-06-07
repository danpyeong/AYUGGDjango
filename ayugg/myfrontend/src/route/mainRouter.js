import {
    createBrowserRouter,
} from "react-router-dom";
import App from "../App";
import SearchPage from "../page/search/searchPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path:"/search/:gameName/:tagLine",
    element:<SearchPage></SearchPage>
  },

]);

export default router;