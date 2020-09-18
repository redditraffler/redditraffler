import React from "react";
import axios from "redaxios";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import "jest-styled-components";

import RaffleMetrics from "./RaffleMetrics";

jest.mock("redaxios");

describe("when the API call is in progress", () => {
  beforeEach(() => {
    axios.get.mockImplementation(async () => {
      await new Promise((resolve) => setTimeout(99999, resolve));
    });
  });

  it("returns the skeleton", async () => {
    const { container } = render(<RaffleMetrics />);

    expect(container.firstChild).toMatchSnapshot();
  });
});

describe("when the API call fails", () => {
  beforeEach(() => {
    axios.get.mockImplementation(async () => {
      throw new Error("oh boy");
    });
  });

  it("returns the error message", async () => {
    const { container } = render(<RaffleMetrics />);
    await screen.findByText(/fetch raffle metrics/);

    expect(container.firstChild).toMatchSnapshot();
  });
});

describe("when the API call is successful", () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({
      data: {
        num_total_verified_raffles: 123,
        num_total_winners: 456,
        num_total_subreddits: 1234,
        top_recent_subreddits: [],
      },
    });
  });

  it("returns the metrics container", async () => {
    const { container } = render(<RaffleMetrics />);
    await screen.findByText(/communities served/);

    expect(container.firstChild).toMatchSnapshot();
  });
});
