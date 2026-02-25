"""
Dashboard Page - Overview and statistics
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QCard, QCardLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.config import *
from src.services.repair_service import RepairService
from src.services.customer_service import CustomerService
from src.services.database import Database


class DashboardPage(QWidget):
    """Dashboard with statistics and overview"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize dashboard"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Dashboard")
        title_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Statistics row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Pending tickets
        pending = self._create_stat_card("Pending Tickets", self._count_pending(), COLOR_WARNING)
        stats_layout.addWidget(pending)
        
        # Active tickets
        active = self._create_stat_card("Active Tickets", self._count_active(), COLOR_PRIMARY)
        stats_layout.addWidget(active)
        
        # Completed this week
        completed = self._create_stat_card("Completed This Week", self._count_completed(), COLOR_SUCCESS)
        stats_layout.addWidget(completed)
        
        # Total customers
        customers = self._create_stat_card("Total Customers", self._count_customers(), COLOR_SECONDARY)
        stats_layout.addWidget(customers)
        
        layout.addLayout(stats_layout)
        
        # Recent activity section
        activity_title = QLabel("Recent Activity")
        activity_font = QFont(FONT_FAMILY, FONT_SIZE_NORMAL, QFont.Weight.Bold)
        activity_title.setFont(activity_font)
        layout.addWidget(activity_title)
        
        # Recent tickets list
        recent_tickets = self._create_recent_tickets()
        layout.addWidget(recent_tickets)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QWidget:
        """Create statistic card"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-left: 4px solid {color};
                border-radius: 4px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_font = QFont(FONT_FAMILY, FONT_SIZE_SMALL)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY};")
        layout.addWidget(title_label)
        
        value_label = QLabel(str(value))
        value_font = QFont(FONT_FAMILY, FONT_SIZE_HEADING, QFont.Weight.Bold)
        value_label.setFont(value_font)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def _create_recent_tickets(self) -> QWidget:
        """Create recent tickets list"""
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        tickets = RepairService.list_tickets()[:5]
        
        if not tickets:
            no_tickets = QLabel("No recent tickets")
            no_tickets.setStyleSheet(f"color: {COLOR_TEXT_SECONDARY};")
            layout.addWidget(no_tickets)
        else:
            for ticket in tickets:
                ticket_row = QLabel(
                    f"Ticket #{ticket['ticket_number']} - {ticket['description'][:50]}... "
                    f"({ticket['status']})"
                )
                ticket_row.setFont(QFont(FONT_FAMILY, FONT_SIZE_NORMAL))
                layout.addWidget(ticket_row)
        
        layout.addStretch()
        container.setLayout(layout)
        return container
    
    def _count_pending(self) -> int:
        """Count pending tickets"""
        tickets = RepairService.list_tickets(STATUS_PENDING)
        return len(tickets)
    
    def _count_active(self) -> int:
        """Count active tickets"""
        tickets = RepairService.list_tickets(STATUS_IN_PROGRESS)
        return len(tickets)
    
    def _count_completed(self) -> int:
        """Count completed tickets this week"""
        # TODO: Filter by date range
        tickets = RepairService.list_tickets(STATUS_COMPLETED)
        return len(tickets)
    
    def _count_customers(self) -> int:
        """Count total customers"""
        customers = CustomerService.list_customers()
        return len(customers)
