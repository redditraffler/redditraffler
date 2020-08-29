import React from "react";
import useAsync from "react-use/lib/useAsync";

import Container from "react-bulma-components/lib/components/container";
import Columns from "react-bulma-components/lib/components/columns";
import Loader from "react-bulma-components/lib/components/loader";
import Heading from "react-bulma-components/lib/components/heading";

import { getRecentRaffles } from "@js/api";
import { colors } from "@js/theme";

import RaffleListItem from "./RaffleListItem";

const RecentRaffles = () => {
  const { loading, error, value: raffles } = useAsync(getRecentRaffles);

  if (loading || error) {
    return (
      <Container>
        <Columns centered>
          <Columns.Column
            size="one-quarter"
            style={{ display: "flex", justifyContent: "center" }}
          >
            {loading ? (
              <Loader
                style={{
                  width: "2rem",
                  height: "2rem",
                  border: `2px solid ${colors.reddit}`,
                  borderTopColor: "transparent",
                  borderRightColor: "transparent",
                }}
              />
            ) : (
              <p>Couldn&apos;t fetch recent raffles :(</p>
            )}
          </Columns.Column>
        </Columns>
      </Container>
    );
  }

  return (
    <Container>
      <Columns centered>
        <Columns.Column size={8}>
          <Heading
            style={{
              display: "flex",
              justifyContent: "center",
              color: colors.reddit,
            }}
          >
            Recent Raffles
          </Heading>
          {raffles.map(
            ({ created_at, submission_title, submission_id, subreddit }) => (
              <RaffleListItem
                key={submission_id}
                created_at={created_at}
                submission_title={submission_title}
                submission_id={submission_id}
                subreddit={subreddit}
              />
            )
          )}
        </Columns.Column>
      </Columns>
    </Container>
  );
};

export default RecentRaffles;
