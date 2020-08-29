import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";

import Box from "react-bulma-components/lib/components/box";
import Element from "react-bulma-components/lib/components/element";
import Tile from "react-bulma-components/lib/components/tile";
import Heading from "react-bulma-components/lib/components/heading";

import { truncateStringAfterLength } from "@js/util";
import { colors } from "@js/theme";

import Emoji from "../Emoji";

dayjs.extend(relativeTime);

const RaffleListItemEmojis = ["🍀", "🎁", "🏆", "🌟", "🏅", "🎉", "🎊"];

const VCenteredTile = styled(Tile)`
  display: flex;
  align-items: center;
`;

const RaffleListItemContainer = styled(Box)`
  && {
    padding-top: 0rem;
    padding-bottom: 0rem;
  }

  transition: all 0.2s ease-in-out;

  a {
    /* Override link styling in app.scss */
    color: ${colors.bulmaDarkGrayText};
  }

  &:hover {
    transform: scale(1.05);
  }
`;

const RaffleListItem = ({
  created_at,
  submission_title,
  submission_id,
  subreddit,
  ...props
}) => {
  const created_at_ms = created_at * 1000;
  const createdAtDayjs = dayjs(created_at_ms);
  // Determine the emoji using the epoch, so each raffle will always have the same emoji assigned to it
  const emojiForRaffleItem =
    RaffleListItemEmojis[
      Math.round(created_at_ms % RaffleListItemEmojis.length)
    ];

  return (
    <RaffleListItemContainer {...props}>
      <a href={`/raffles/${submission_id}`}>
        <Tile kind="ancestor">
          <Tile kind="parent" size={1}>
            <VCenteredTile kind="child">
              <Emoji
                symbol={emojiForRaffleItem}
                style={{ display: "block", fontSize: "3rem" }}
              />
            </VCenteredTile>
          </Tile>
          <Tile kind="parent">
            <VCenteredTile kind="child">
              <div>
                <Element
                  renderAs="p"
                  className="is-size-6 has-text-weight-medium"
                  style={{ marginBottom: "0.5rem" }}
                  title={submission_title}
                >
                  {truncateStringAfterLength(100, submission_title)}
                </Element>
                <Heading heading renderAs="p">
                  /r/{subreddit}
                </Heading>
              </div>
            </VCenteredTile>
          </Tile>
          <Tile kind="parent" size={2}>
            <VCenteredTile kind="child" style={{ justifyContent: "flex-end" }}>
              <Element
                renderAs="p"
                className="is-size-7"
                title={createdAtDayjs.toString()}
              >
                {createdAtDayjs.from(dayjs())}
              </Element>
            </VCenteredTile>
          </Tile>
        </Tile>
      </a>
    </RaffleListItemContainer>
  );
};

RaffleListItem.propTypes = {
  created_at: PropTypes.number.isRequired,
  submission_title: PropTypes.string.isRequired,
  submission_id: PropTypes.string.isRequired,
  subreddit: PropTypes.string.isRequired,
};

export default RaffleListItem;
