import { FC } from "react";
import { HydrationBoundary } from "@tanstack/react-query";

type Props = {
  children: React.ReactNode;
  state: unknown;
};

const Hydrate: FC<Props> = ({ children, state }) => {
  return <HydrationBoundary state={state}>{children}</HydrationBoundary>;
};

export default Hydrate;
