import { applyMiddleware, combineReducers, createStore } from "redux";
import accountReducer from "./features/accounts/accountSlice";
import customerReducer from "./features/customers/customerSlice";
import { thunk } from "redux-thunk";
import { composeWithDevTools } from "redux-devtools-extension";

const rootReducer = combineReducers({
  account: accountReducer,
  customer: customerReducer,
});

const store = createStore(rootReducer, composeWithDevTools(applyMiddleware(thunk)));

export default store;

// store.dispatch({ type: "account/deposit", payload: 1000 });
// console.log(store.getState());

// store.dispatch({ type: "account/withdrawal", payload: 500 });
// console.log(store.getState());

// store.dispatch({ type: "account/requestLoan", payload: {amount:1000, purpose:"vacation"} });
// console.log(store.getState());

// store.dispatch({ type: "account/payLoan" });
// console.log(store.getState());

// store.dispatch({ type: "account/withdrawal", payload: 500 });
// console.log(store.getState());

// store.dispatch(deposit(1000));
// console.log(store.getState());

// store.dispatch(withdrawal(500));
// console.log(store.getState());

// store.dispatch(requestLoan(1000, "vacation"));
// console.log(store.getState());

// store.dispatch(payLoan());
// console.log(store.getState());

// store.dispatch(createCustomer("John Doe", "123456789"));
// console.log(store.getState());

// store.dispatch(deposit(1000));
// console.log(store.getState());

// store.dispatch(updateCustomer("Jane Doe"));
// console.log(store.getState());
