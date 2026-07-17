package com.testable.training;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RiskPrioritizerTest {

    private RiskPrioritizer prioritizer;

    @BeforeEach
    void setUp() {
        prioritizer = new RiskPrioritizer();
    }

    @Test
    void computeChurnScore() {
        assertEquals(15, prioritizer.computeChurnScore(10, 5));
    }

    @Test
    void requiresRegressionTestAboveThreshold() {
        assertTrue(prioritizer.requiresRegressionTest(50, 10));
    }

    @Test
    void requiresRegressionTestBelowThreshold() {
        assertFalse(prioritizer.requiresRegressionTest(5, 10));
    }

    @Test
    void prioritizeByChurnOrdersHighestFirst() {
        List<RiskPrioritizer.ChurnRecord> records = List.of(
                new RiskPrioritizer.ChurnRecord("OrderService.java", 5, 2),
                new RiskPrioritizer.ChurnRecord("PaymentValidator.java", 20, 10),
                new RiskPrioritizer.ChurnRecord("RiskPrioritizer.java", 8, 4)
        );
        assertEquals(
                List.of("PaymentValidator.java", "RiskPrioritizer.java", "OrderService.java"),
                prioritizer.prioritizeByChurn(records)
        );
    }
}
