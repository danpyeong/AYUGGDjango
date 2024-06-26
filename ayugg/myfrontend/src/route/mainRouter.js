import {
    createBrowserRouter,
} from "react-router-dom";
import App from "../App";
import Multi from "../view/page/multi/multiPage";
import ChampionsMain from "../view/page/champions/championsMain";
import StatisticsMain from "../view/page/statistics/statisticsMain";
import SearchPage from "../view/page/search/searchPage";
import ChampionsDetails from "../view/page/details/detailsMain";
import RankingDetail from "../view/page/ranking/rankingDetailSolo";
import RankingMain from "../view/page/ranking/rankingMain";
import RankingDetailFlex from "../view/page/ranking/rankingDetailFlex";

// import Multi from "../../view/page/multi/multiPage"  

const router = createBrowserRouter([
    {
      path: "/",
      element: <App />,
    },
    {
      path:"/champions",
      element: <ChampionsMain></ChampionsMain>
    },
    {
      path:"/statistics",
      element:<StatisticsMain></StatisticsMain>
    },
    {
      path:"/ranking",
      element:<RankingMain></RankingMain>
    },
    {
      path:"/ranking/solo",
      element:<RankingDetail></RankingDetail>
    },
    {
      path:"/ranking/flex",
      element:<RankingDetailFlex></RankingDetailFlex>
    },
    {
      path:"/multi",
      element:<Multi></Multi>
    },
    {
      path:"/search/:gameName/:tagLine",
      element:<SearchPage></SearchPage>
    },
    {
      path:"/champions/:id",
      element:<ChampionsDetails></ChampionsDetails>
    },
]);

export default router;