import React from "react";
import useAsync from "react-use/lib/useAsync";
import Skeleton from "react-loading-skeleton";
import styled from "styled-components";
import Columns from "react-bulma-components/lib/components/columns";
import Box from "react-bulma-components/lib/components/box";
import Container from "react-bulma-components/lib/components/container";
import Heading from "react-bulma-components/lib/components/heading";
import Tile from "react-bulma-components/lib/components/tile";

import { getRaffleStats } from "@js/api";
import { colors } from "@js/theme";

const StatHeading = styled(Heading)`
  color: ${colors.reddit};
  text-align: center;
`;

const EqualHeightBox = styled(Box)`
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 10px;
`;

const RaffleStats = () => {
  const { loading, error, value: metrics } = useAsync(getRaffleStats);

  if (error) {
    return (
      <Container>
        <Columns centered>
          <Columns.Column size="one-quarter">
            <Box size="one-quarter">Couldn&apos;t fetch raffle stats :(</Box>
          </Columns.Column>
        </Columns>
      </Container>
    );
  }

  const stats = [
    {
      displayValue: metrics?.num_total_subreddits?.toLocaleString(),
      label: "communities served",
    },
    {
      displayValue: metrics?.num_total_verified_raffles?.toLocaleString(),
      label: "raffles created",
    },
    {
      displayValue: metrics?.num_total_winners?.toLocaleString(),
      label: "lucky winners",
    },
  ];

  return (
    <Container>
      <Columns centered breakpoint="desktop">
        <Columns.Column size={6}>
          <EqualHeightBox>
            <Tile kind="parent" style={{ alignItems: "center" }}>
              {loading ? (
                <Tile kind="child">
                  <Skeleton count={2} height={30} />
                </Tile>
              ) : (
                <React.Fragment>
                  {stats.map(({ displayValue, label }) => {
                    return (
                      <Tile kind="child" key={label}>
                        <StatHeading>{displayValue}</StatHeading>
                        <Heading subtitle style={{ textAlign: "center" }}>
                          {label}
                        </Heading>
                      </Tile>
                    );
                  })}
                </React.Fragment>
              )}
            </Tile>
          </EqualHeightBox>
        </Columns.Column>
      </Columns>
    </Container>
  );
};

export default RaffleStats;
