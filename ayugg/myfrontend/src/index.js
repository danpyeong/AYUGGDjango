import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { Provider } from 'react-redux';
import { RouterProvider } from "react-router-dom";
import { store } from './redux/store';
import router from '../src/route/mainRouter';
// c:\Users\Administrator\Desktop\AYUGGSERVER\ayugg\myfrontend\src\route\mainRouter.js

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router}></RouterProvider>
    </Provider>
  </React.StrictMode>
);

reportWebVitals();
