package com.testable.training;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class InventoryServiceTest {

    private final InventoryService service = new InventoryService();

    @Test
    void availableUnits() {
        assertEquals(7, service.availableUnits(10, 3));
        assertEquals(0, service.availableUnits(2, 5));
    }

    @Test
    void stockStatus() {
        assertEquals("out_of_stock", service.stockStatus(0));
        assertEquals("low", service.stockStatus(3));
        assertEquals("ok", service.stockStatus(20));
    }

    @Test
    void allocateSku() {
        List<String> slots = service.allocateSku("ABC", 2);
        assertEquals(2, slots.size());
        assertTrue(slots.get(0).startsWith("ABC-BIN-"));
    }
}
